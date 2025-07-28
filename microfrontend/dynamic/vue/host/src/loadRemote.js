import {
    __federation_method_setRemote,
    __federation_method_getRemote,
    __federation_method_unwrapDefault
  } from 'virtual:__federation__'

  export async function loadRemote(remoteName, exposedModule) {
    await __federation_method_setRemote(remoteName, {
      url: `/remote/remoteEntry.js`,
      format: 'esm',
      from: 'vite',
      remoteType: 'module'
    })
    // url: `${remoteUrl}/assets/remoteEntry.js`,
  
    const mod = await __federation_method_getRemote(remoteName, exposedModule)
    return __federation_method_unwrapDefault(mod)
  }