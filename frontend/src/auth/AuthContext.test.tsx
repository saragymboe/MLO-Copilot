import { render, screen } from '@testing-library/react';
import { AuthProvider, useAuth } from './AuthContext';

function Probe() {
  const { user } = useAuth();
  return <div>{user ? 'signed-in' : 'signed-out'}</div>;
}

describe('AuthContext', () => {
  it('renders signed-out when unauthenticated', () => {
    render(<AuthProvider><Probe /></AuthProvider>);
    expect(screen.getByText(/signed-out/i)).toBeInTheDocument();
  });
});
