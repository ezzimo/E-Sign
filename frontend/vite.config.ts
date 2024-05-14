import { TanStackRouterVite } from "@tanstack/router-vite-plugin";
import react from "@vitejs/plugin-react-swc";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react(), TanStackRouterVite()],
    server: {
        fs: {
            strict: false // Allow serving files outside the project root
        }
    },
    build: {
        outDir: 'dist' // Specify the output directory for the build
    },
    publicDir: 'public' // Specify the public directory for static files
});
