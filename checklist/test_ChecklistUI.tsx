import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import ChecklistUI from './ChecklistUI';

describe('ChecklistUI', () => {
  it('renders input fields and create button', () => {
    render(<ChecklistUI token="testtoken" />);
    expect(screen.getByPlaceholderText('Description')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Assign to user')).toBeInTheDocument();
    expect(screen.getByText('Create Task')).toBeInTheDocument();
  });
});
