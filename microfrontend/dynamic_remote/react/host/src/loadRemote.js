// import {
//     __federation_method_setRemote,
//     __federation_method_getRemote,
//     __federation_method_unwrapDefault
// } from 'virtual:__federation__'

// export async function loadRemote(remoteName, remoteUrl, exposedModule) {
//     await __federation_method_setRemote(remoteName, {
//       url: `${remoteUrl}/assets/remoteEntry.js`,
//       format: 'esm',
//       from: 'vite',
//       remoteType: 'module'
//     })
  
//     const mod = await __federation_method_getRemote(remoteName, exposedModule)
//     return __federation_method_unwrapDefault(mod)
// }

import {
  __federation_method_setRemote as setRemote,
  __federation_method_getRemote as getRemote,
  __federation_method_unwrapDefault as unwrapDefault,
} from 'virtual:__federation__';

export async function loadRemote(remoteName, remoteUrl, exposedModule) {
  setRemote(remoteName, {
    url: `${remoteUrl}/assets/remoteEntry.js`,
    format: 'esm',
  });

  const module = await getRemote(remoteName, exposedModule);
  return unwrapDefault(module);
}