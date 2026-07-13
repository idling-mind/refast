import { describe, it, expect, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { Form } from '../shadcn/form';

describe('Form Component', () => {
  it('submits values of disabled input fields', () => {
    const onSubmit = vi.fn();
    render(
      <Form onSubmit={onSubmit}>
        <input type="text" name="enabled_input" defaultValue="enabled_val" />
        <input type="text" name="disabled_input" defaultValue="disabled_val" disabled />
        <textarea name="disabled_textarea" defaultValue="disabled_area_val" disabled />
        <select name="disabled_select" defaultValue="opt2" disabled>
          <option value="opt1">Option 1</option>
          <option value="opt2">Option 2</option>
        </select>
        <input type="checkbox" name="disabled_checked_checkbox" value="checkbox_val" defaultChecked disabled />
        <input type="checkbox" name="disabled_unchecked_checkbox" value="checkbox_val" disabled />
        <button type="submit" data-testid="submit-btn">Submit</button>
      </Form>
    );

    const submitBtn = screen.getByTestId('submit-btn');
    fireEvent.click(submitBtn);

    expect(onSubmit).toHaveBeenCalledTimes(1);
    expect(onSubmit).toHaveBeenCalledWith({
      enabled_input: 'enabled_val',
      disabled_input: 'disabled_val',
      disabled_textarea: 'disabled_area_val',
      disabled_select: 'opt2',
      disabled_checked_checkbox: 'checkbox_val',
    });
  });

  it('excludes values of disabled input fields when includeDisabled is false', () => {
    const onSubmit = vi.fn();
    render(
      <Form onSubmit={onSubmit} includeDisabled={false}>
        <input type="text" name="enabled_input" defaultValue="enabled_val" />
        <input type="text" name="disabled_input" defaultValue="disabled_val" disabled />
        <textarea name="disabled_textarea" defaultValue="disabled_area_val" disabled />
        <button type="submit" data-testid="submit-btn">Submit</button>
      </Form>
    );

    const submitBtn = screen.getByTestId('submit-btn');
    fireEvent.click(submitBtn);

    expect(onSubmit).toHaveBeenCalledTimes(1);
    expect(onSubmit).toHaveBeenCalledWith({
      enabled_input: 'enabled_val',
    });
  });
});
