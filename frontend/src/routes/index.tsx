import { Navigate, Route, Routes } from 'react-router-dom';
import { AuthGuard } from '../components/AuthGuard';
import { AdminGuard } from '../components/AdminGuard';
import { AppShell } from '../components/AppShell';
import { LoginPage } from '../pages/Login';
import { OAuthCallbackPage } from '../pages/OAuthCallback';
import { DashboardPage } from '../pages/Dashboard';
import { ProductLibraryPage } from '../pages/ProductLibrary';
import { ProductDetailPage } from '../pages/ProductDetail';
import { ScenarioFinderPage } from '../pages/ScenarioFinder';
import { ChatPage } from '../pages/Chat';
import { ConversationHistoryPage } from '../pages/ConversationHistory';
import { AdminProductsPage } from '../pages/AdminProducts';
import { SettingsPage } from '../pages/Settings';
import { NotFoundPage } from '../pages/NotFound';

export function AppRoutes() {
  return (
    <AppShell>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/oauth/callback" element={<OAuthCallbackPage />} />
        <Route element={<AuthGuard />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/products" element={<ProductLibraryPage />} />
          <Route path="/products/:productId" element={<ProductDetailPage />} />
          <Route path="/scenarios" element={<ScenarioFinderPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/conversations" element={<ConversationHistoryPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route element={<AdminGuard />}>
            <Route path="/admin/products" element={<AdminProductsPage />} />
          </Route>
        </Route>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </AppShell>
  );
}
