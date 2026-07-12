import { Button, Paper, Stack, Typography } from '@mui/material';
import { useAuth } from '../auth/AuthContext';
import { DisclaimerBanner } from '../components/DisclaimerBanner';

export function LoginPage() {
  const { signIn } = useAuth();
  return (
    <Paper sx={{ p: 4, maxWidth: 560, mx: 'auto' }}>
      <Stack spacing={2}>
        <Typography variant="h4">Sign in</Typography>
        <Typography color="text.secondary">Use your Microsoft or Google account to access product guidance and recommendations.</Typography>
        <Button variant="contained" onClick={() => signIn()}>Continue with Google</Button>
        <DisclaimerBanner />
      </Stack>
    </Paper>
  );
}
