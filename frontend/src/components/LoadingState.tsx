import { CircularProgress, Stack, Typography } from '@mui/material';

export function LoadingState() {
  return (
    <Stack spacing={2} alignItems="center" sx={{ py: 4 }}>
      <CircularProgress />
      <Typography>Loading…</Typography>
    </Stack>
  );
}
