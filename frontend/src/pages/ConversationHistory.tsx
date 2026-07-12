import { Paper, Typography } from '@mui/material';
import { ConversationList } from '../components/ConversationList';

export function ConversationHistoryPage() {
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>Conversation History</Typography>
      <ConversationList />
    </Paper>
  );
}
