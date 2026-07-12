import { Paper, Typography } from '@mui/material';

export function SettingsPage() {
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5">Settings</Typography>
      <Typography color="text.secondary">Manage your notification preferences and account details.</Typography>
    </Paper>
  );
}
