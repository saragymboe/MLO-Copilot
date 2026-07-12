import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

describe('app shell', () => {
  it('renders the application shell', () => {
    render(
      <MemoryRouter>
        <App />
      </MemoryRouter>,
    );
    expect(screen.getByText(/Mortgage Product Copilot/i)).toBeInTheDocument();
  });
});
