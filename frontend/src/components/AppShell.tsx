import {
  AppBar,
  Box,
  Button,
  Container,
  Toolbar,
  Typography,
} from "@mui/material";
import type { ReactNode } from "react";
import { Link as RouterLink } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export function AppShell({ children }: { children: ReactNode }) {
  const { user, signOutUser } = useAuth();
  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "#f7f8fb" }}>
      <AppBar
        position="static"
        color="transparent"
        elevation={0}
        sx={{ borderBottom: "1px solid #e5e7eb" }}
      >
        <Toolbar>
          <Typography
            variant="h6"
            component={RouterLink}
            to="/"
            sx={{ color: "#14213d", textDecoration: "none", flexGrow: 1 }}
          >
            Mortgage Product Copilot
          </Typography>
          {user ? (
            <Button onClick={() => signOutUser()}>Sign Out</Button>
          ) : (
            <Button component={RouterLink} to="/login">
              Sign In
            </Button>
          )}
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {children}
      </Container>
    </Box>
  );
}
