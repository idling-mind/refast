import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useStateManager, findComponent, getComponentPath } from '../StateManager';
import { ComponentTree, UpdateMessage } from '../../types';

describe('useStateManager', () => {
  it('initializes with null tree', () => {
    const { result } = renderHook(() => useStateManager());
    expect(result.current.componentTree).toBeNull();
    expect(result.current.appState).toEqual({});
  });

  it('initializes with provided tree', () => {
    const initialTree: ComponentTree = {
      type: 'Container',
      id: 'root',
      props: {},
      children: [],
    };
    const { result } = renderHook(() => useStateManager(initialTree));
    expect(result.current.componentTree).toEqual(initialTree);
  });

  it('updates component tree', () => {
    const { result } = renderHook(() => useStateManager());
    const newTree: ComponentTree = {
      type: 'Container',
      id: 'new-root',
      props: {},
      children: [],
    };

    act(() => {
      result.current.setComponentTree(newTree);
    });

    expect(result.current.componentTree).toEqual(newTree);
  });

  it('updates app state', () => {
    const { result } = renderHook(() => useStateManager());

    act(() => {
      result.current.setAppState({ count: 1 });
    });

    expect(result.current.appState).toEqual({ count: 1 });

    act(() => {
      result.current.setAppState({ name: 'test' });
    });

    expect(result.current.appState).toEqual({ count: 1, name: 'test' });
  });

  it('gets app state value', () => {
    const { result } = renderHook(() => useStateManager());

    act(() => {
      result.current.setAppState({ count: 42 });
    });

    expect(result.current.getAppState('count')).toBe(42);
    expect(result.current.getAppState('missing', 'default')).toBe('default');
  });

  it('handles update message - state_update', () => {
    const { result } = renderHook(() => useStateManager());

    const message: UpdateMessage = {
      type: 'state_update',
      state: { counter: 10 },
    };

    act(() => {
      result.current.handleUpdate(message);
    });

    expect(result.current.appState).toEqual({ counter: 10 });
  });
});

describe('findComponent', () => {
  const tree: ComponentTree = {
    type: 'Container',
    id: 'root',
    props: {},
    children: [
      {
        type: 'Row',
        id: 'row-1',
        props: {},
        children: [
          {
            type: 'Button',
            id: 'btn-1',
            props: {},
            children: ['Click'],
          },
        ],
      },
    ],
  };

  it('finds root component', () => {
    const result = findComponent(tree, 'root');
    expect(result?.id).toBe('root');
  });

  it('finds nested component', () => {
    const result = findComponent(tree, 'btn-1');
    expect(result?.id).toBe('btn-1');
  });

  it('returns null for non-existent component', () => {
    const result = findComponent(tree, 'non-existent');
    expect(result).toBeNull();
  });
});

describe('getComponentPath', () => {
  const tree: ComponentTree = {
    type: 'Container',
    id: 'root',
    props: {},
    children: [
      {
        type: 'Row',
        id: 'row-1',
        props: {},
        children: [
          {
            type: 'Button',
            id: 'btn-1',
            props: {},
            children: [],
          },
        ],
      },
    ],
  };

  it('gets path to root', () => {
    const path = getComponentPath(tree, 'root');
    expect(path).toEqual(['root']);
  });

  it('gets path to nested component', () => {
    const path = getComponentPath(tree, 'btn-1');
    expect(path).toEqual(['root', 'row-1', 'btn-1']);
  });

  it('returns null for non-existent component', () => {
    const path = getComponentPath(tree, 'non-existent');
    expect(path).toBeNull();
  });
});
