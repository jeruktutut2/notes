# MICRO FRONT END

## install
    npm create vite@latest host
    cd host
    npm install
    npm install tailwindcss @tailwindcss/vite
    npm install -D @originjs/vite-plugin-federation

    npm create vite@latest remote
    cd remote
    npm install
    npm install -D tailwindcss @tailwindcss/vite @originjs/vite-plugin-federation

    npm install vue-router@4
    npm i react-router-dom
    react: { singleton: true, eager: true },
    'react-dom': { singleton: true, eager: true }

    to run remote on host, you have to npm run build and npm run preview remote app, remoteEntry.js is in dist/assets/remoteEntry, use this (http://localhost:3001/assets/remoteEntry.js) on vite config host

    since tailwindcss not supported yet for vue3, please see the tailwindcss doc to install tailwindcss on vue3
