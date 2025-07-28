export async function loadRemoteComponent(remoteUrl, remoteName, exposedModule) {
  // Load remote script
  await new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = remoteUrl;
    script.type = 'text/javascript';
    script.async = true;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });

  // Init shared scope
  await __webpack_init_sharing__('default');
  const container = window[remoteName];

  if (!container) {
    throw new Error(`Remote ${remoteName} is not available on window.`);
  }

  if (!container.init) {
    throw new Error(`Remote container ${remoteName} has no 'init' method`);
  }

  await container.init(__webpack_share_scopes__.default);
  const factory = await container.get(exposedModule);
  const Module = factory();
  return Module;
}
