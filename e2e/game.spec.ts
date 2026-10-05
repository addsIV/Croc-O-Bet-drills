import { test, expect } from '@playwright/test';

// 牙齒 4 在 layout 的位置（百分比），canvas 是正方形所以 x y 都用同一個比例
const TOOTH_4 = { x: 0.523, y: 0.27 };

test('player can place a bet, press a tooth and cash out', async ({ page }) => {
  await page.goto('/');
  await page.waitForTimeout(500); // 等 canvas 畫好

  await page.getByRole('button', { name: 'BET NOW' }).click();

  const canvas = page.locator('canvas');
  const box = await canvas.boundingBox();
  if (!box) throw new Error('canvas not found');
  await page.mouse.click(box.x + box.width * TOOTH_4.x, box.y + box.height * TOOTH_4.y);

  // 壓到一顆牙之後倍率應該大於 1，Cash Out 應該可以按
  const cashOut = page.getByRole('button', { name: /CASH OUT/ });
  await expect(cashOut).toBeEnabled();
  await cashOut.click();

  await expect(page.getByText(/\+\$/)).toBeVisible();
});

test('balance is deducted when betting', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'BET NOW' }).click();
  await expect(page.getByText('$990.00')).toBeVisible();
});
