import { Paper } from '@mui/material';
import { ChatPanel } from '../components/ChatPanel';
import { DisclaimerBanner } from '../components/DisclaimerBanner';

export function ChatPage() {
  return (
    <div>
      <DisclaimerBanner />
      <Paper sx={{ p: 3 }}>
        <ChatPanel />
      </Paper>
    </div>
  );
}
