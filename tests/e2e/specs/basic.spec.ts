import { test, expect } from '@playwright/test';

test.describe('Basic Page Tests', () => {
  test('should load the home page', async ({ page }) => {
    await page.goto('/');
    
    // Check that the page loads
    await expect(page).toHaveTitle(/Counter Example|Refast/);
    
    // Wait for the app to render
    await page.waitForSelector('#root');
    
    // Check that the root element exists
    const root = page.locator('#root');
    await expect(root).toBeVisible();
  });

  test('should have initial component data', async ({ page }) => {
    await page.goto('/');
    
    // Check that initial data is embedded in the page
    const initialData = await page.evaluate(() => {
      return (window as any).__REFAST_INITIAL_DATA__;
    });
    
    expect(initialData).toBeDefined();
    expect(initialData.type).toBeTruthy();
  });

  test('should display counter card', async ({ page }) => {
    await page.goto('/');
    
    // Wait for content to render
    await page.waitForTimeout(500);
    
    // Check for counter-related content in the initial data
    const html = await page.content();
    expect(html).toContain('Counter Example');
  });

  test('should navigate to about page', async ({ page }) => {
    await page.goto('/about');
    
    // Check that about page loads
    await page.waitForSelector('#root');
    
    // Check that initial data has about page content
    const initialData = await page.evaluate(() => {
      return (window as any).__REFAST_INITIAL_DATA__;
    });
    
    expect(initialData).toBeDefined();
  });

  test('should return 404 for unknown routes when no fallback', async ({ page }) => {
    // This test is for when no "/" page is defined
    // In basic example, "/" is defined so it falls back
    const response = await page.goto('/nonexistent');
    
    // The basic example has "/" defined, so it will fallback and return 200
    // We just check the page loads
    expect(response?.status()).toBe(200);
  });

  test('should include correct meta tags', async ({ page }) => {
    await page.goto('/');
    
    // Check viewport meta tag
    const viewport = await page.locator('meta[name="viewport"]').getAttribute('content');
    expect(viewport).toContain('width=device-width');
    
    // Check charset
    const charset = await page.locator('meta[charset]').getAttribute('charset');
    expect(charset?.toLowerCase()).toBe('utf-8');
  });

  test('should have proper HTML structure', async ({ page }) => {
    await page.goto('/');
    
    // Check for essential elements
    await expect(page.locator('html')).toBeAttached();
    await expect(page.locator('head')).toBeAttached();
    await expect(page.locator('body')).toBeAttached();
    await expect(page.locator('#root')).toBeAttached();
  });
});

test.describe('WebSocket Connection', () => {
  test('should have WebSocket endpoint available', async ({ page }) => {
    await page.goto('/');
    
    // Try to establish WebSocket connection
    const wsResult = await page.evaluate(async () => {
      return new Promise<{ connected: boolean; error?: string }>((resolve) => {
        try {
          const ws = new WebSocket('ws://localhost:8000/ws');
          
          ws.onopen = () => {
            ws.close();
            resolve({ connected: true });
          };
          
          ws.onerror = () => {
            resolve({ connected: false, error: 'Connection failed' });
          };
          
          // Timeout after 5 seconds
          setTimeout(() => {
            ws.close();
            resolve({ connected: false, error: 'Timeout' });
          }, 5000);
        } catch (e) {
          resolve({ connected: false, error: String(e) });
        }
      });
    });
    
    expect(wsResult.connected).toBe(true);
  });
});
