import { Dialog, DialogActions, DialogContent, DialogTitle, Button } from '@mui/material';

export function ConfirmDialog({ open, title, message, onClose }: { open: boolean; title: string; message: string; onClose: () => void }) {
  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>{message}</DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={onClose} color="warning">Continue</Button>
      </DialogActions>
    </Dialog>
  );
}
