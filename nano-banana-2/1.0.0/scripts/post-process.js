#!/usr/bin/env node
/**
 * Post-process generated images: resize, add watermark, compress
 * Usage: node post-process.js <input.png> [output.jpg]
 */

const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

const PLUGIN_ROOT = path.resolve(__dirname, '..');
const WATERMARK_DARK = path.join(PLUGIN_ROOT, 'skills/nano-banana-2/assets/sas-logo-dark.png');
const WATERMARK_LIGHT = path.join(PLUGIN_ROOT, 'skills/nano-banana-2/assets/sas-logo-light.png');

async function postProcess(inputPath, outputPath) {
  // Validate input exists
  if (!fs.existsSync(inputPath)) {
    console.error(`Error: Input file not found: ${inputPath}`);
    process.exit(1);
  }

  // Validate watermarks exist
  if (!fs.existsSync(WATERMARK_DARK) || !fs.existsSync(WATERMARK_LIGHT)) {
    console.error('Error: Watermark assets not found');
    console.error(`  Expected: ${WATERMARK_DARK}`);
    console.error(`  Expected: ${WATERMARK_LIGHT}`);
    process.exit(1);
  }

  console.log(`Processing: ${inputPath}`);

  // First resize the image
  const resized = await sharp(inputPath)
    .resize(1000, 1000, { fit: 'inside' })
    .toBuffer({ resolveWithObject: true });

  const { width, height } = resized.info;
  console.log(`  Resized to: ${width}x${height}`);

  // Analyze bottom-right corner brightness (where watermark will go)
  const cornerSize = Math.min(150, Math.floor(width * 0.15), Math.floor(height * 0.15));
  const corner = await sharp(resized.data)
    .extract({
      left: width - cornerSize,
      top: height - cornerSize,
      width: cornerSize,
      height: cornerSize
    })
    .stats();

  // Calculate average brightness from RGB channels
  const avgBrightness = (corner.channels[0].mean + corner.channels[1].mean + corner.channels[2].mean) / 3;

  // Choose watermark: light logo for dark backgrounds, dark logo for light backgrounds
  const isDark = avgBrightness < 128;
  const watermarkPath = isDark ? WATERMARK_LIGHT : WATERMARK_DARK;
  console.log(`  Corner brightness: ${avgBrightness.toFixed(1)} (using ${isDark ? 'light' : 'dark'} watermark)`);

  // Resize watermark preserving transparency
  const watermark = await sharp(watermarkPath)
    .resize(120, 120, { fit: 'inside' })
    .png()
    .toBuffer();

  // Composite and output as JPG
  await sharp(resized.data)
    .composite([{ input: watermark, gravity: 'southeast' }])
    .jpeg({ quality: 85, mozjpeg: true })
    .toFile(outputPath);

  // Get file size
  const stats = fs.statSync(outputPath);
  const sizeKB = (stats.size / 1024).toFixed(1);
  console.log(`  Output: ${outputPath} (${sizeKB} KB)`);

  return { width, height, sizeKB, isDark };
}

// CLI entry point
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Usage: node post-process.js <input.png> [output.jpg]');
    console.log('');
    console.log('If output is not specified, creates <input>_final.jpg');
    process.exit(0);
  }

  const inputPath = args[0];
  let outputPath = args[1];

  if (!outputPath) {
    const parsed = path.parse(inputPath);
    outputPath = path.join(parsed.dir, `${parsed.name}_final.jpg`);
  }

  try {
    await postProcess(inputPath, outputPath);
    console.log('Done!');
  } catch (err) {
    console.error('Error processing image:', err.message);
    process.exit(1);
  }
}

main();
