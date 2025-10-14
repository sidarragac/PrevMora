import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

// Rutas públicas que no requieren autenticación
const isPublicRoute = createRouteMatcher([
  '/sign-in(.*)', // Página de login
  '/', // Página principal
  '/prestamos', // Página de préstamos
  '/pagar-prestamo', // Página de pago de préstamo
]);

// Rutas protegidas
const isProtectedRoute = createRouteMatcher(['/plataforma(.*)', '/api(.*)']);

export default clerkMiddleware(async (auth, req) => {
  // Si la ruta es pública, permitir acceso sin autenticación
  if (isPublicRoute(req)) {
    return;
  }

  // Si la ruta es protegida, verificar autenticación
  const { userId, redirectToSignIn } = await auth();
  if (!userId && isProtectedRoute(req)) {
    return redirectToSignIn();
  }
});

export const config = {
  matcher: [
    // Excluye archivos estáticos y Next.js internals
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|zip|webmanifest)).*)',
    // Siempre ejecuta el middleware para rutas API y TRPC
    '/(api|trpc)(.*)',
  ],
};
