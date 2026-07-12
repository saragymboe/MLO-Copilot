import { List, ListItem, ListItemText } from '@mui/material';

export function ConversationList() {
  return (
    <List>
      <ListItem><ListItemText primary="Recent conversation" secondary="No conversations yet" /></ListItem>
    </List>
  );
}
