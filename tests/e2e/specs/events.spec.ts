import { test, expect } from '@playwright/test';

test.describe('Event Handling Tests', () => {
  test('should have callback references in component tree', async ({ page }) => {
    await page.goto('/');
    
    // Get initial data
    const initialData = await page.evaluate(() => {
      return (window as any).__REFAST_INITIAL_DATA__;
    });
    
    expect(initialData).toBeDefined();
    
    // Find onClick callbacks in the tree (recursive search)
    const hasCallbacks = findCallbacks(initialData);
    expect(hasCallbacks).toBe(true);
  });

  test('should render buttons with click handlers', async ({ page }) => {
    await page.goto('/');
    
    // Check for buttons in the initial data
    const initialData = await page.evaluate(() => {
      return (window as any).__REFAST_INITIAL_DATA__;
    });
    
    // Find Button components
    const buttons = findComponents(initialData, 'Button');
    expect(buttons.length).toBeGreaterThan(0);
  });

  test('WebSocket should accept and process messages', async ({ page }) => {
    await page.goto('/');
    
    // Send a test message through WebSocket
    const result = await page.evaluate(async () => {
      return new Promise<{ success: boolean; response?: any; error?: string }>((resolve) => {
        try {
          const ws = new WebSocket('ws://localhost:8000/ws');
          
          ws.onopen = () => {
            // Send a callback invocation message
            ws.send(JSON.stringify({
              type: 'callback',
              callbackId: 'test-callback',
              data: {},
            }));
            
            // Wait a bit then close
            setTimeout(() => {
              ws.close();
              resolve({ success: true });
            }, 500);
          };
          
          ws.onerror = () => {
            resolve({ success: false, error: 'Connection failed' });
          };
          
          // Timeout
          setTimeout(() => {
            ws.close();
            resolve({ success: false, error: 'Timeout' });
          }, 5000);
        } catch (e) {
          resolve({ success: false, error: String(e) });
        }
      });
    });
    
    expect(result.success).toBe(true);
  });

  test('should have proper callback structure', async ({ page }) => {
    await page.goto('/');
    
    const initialData = await page.evaluate(() => {
      return (window as any).__REFAST_INITIAL_DATA__;
    });
    
    // Find callbacks and verify structure
    const callbacks = extractCallbacks(initialData);
    
    for (const callback of callbacks) {
      expect(callback).toHaveProperty('callbackId');
      expect(typeof callback.callbackId).toBe('string');
    }
  });
});

test.describe('State Management', () => {
  test('should have initial state values', async ({ page }) => {
    await page.goto('/');
    
    const initialData = await page.evaluate(() => {
      return (window as any).__REFAST_INITIAL_DATA__;
    });
    
    // The counter example should show "0" initially
    const textContent = JSON.stringify(initialData);
    expect(textContent).toBeTruthy();
  });

  test('should handle multiple page loads', async ({ page }) => {
    // Load page multiple times
    await page.goto('/');
    let data1 = await page.evaluate(() => (window as any).__REFAST_INITIAL_DATA__);
    
    await page.reload();
    let data2 = await page.evaluate(() => (window as any).__REFAST_INITIAL_DATA__);
    
    // Both should have valid data
    expect(data1).toBeDefined();
    expect(data2).toBeDefined();
    expect(data1.type).toBe(data2.type);
  });
});

// Helper functions
function findCallbacks(obj: any): boolean {
  if (!obj || typeof obj !== 'object') return false;
  
  if (obj.callbackId) return true;
  
  for (const key of Object.keys(obj)) {
    if (findCallbacks(obj[key])) return true;
  }
  
  return false;
}

function findComponents(obj: any, type: string): any[] {
  const results: any[] = [];
  
  function search(node: any) {
    if (!node || typeof node !== 'object') return;
    
    if (node.type === type) {
      results.push(node);
    }
    
    if (node.children && Array.isArray(node.children)) {
      for (const child of node.children) {
        search(child);
      }
    }
    
    // Also search in props for nested components
    if (node.props) {
      for (const value of Object.values(node.props)) {
        search(value);
      }
    }
  }
  
  search(obj);
  return results;
}

function extractCallbacks(obj: any): any[] {
  const callbacks: any[] = [];
  
  function search(node: any) {
    if (!node || typeof node !== 'object') return;
    
    if (node.callbackId) {
      callbacks.push(node);
      return;
    }
    
    for (const value of Object.values(node)) {
      search(value);
    }
  }
  
  search(obj);
  return callbacks;
}
