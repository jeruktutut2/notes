// import {
//     __federation_method_setRemote,
//     __federation_method_getRemote,
//     __federation_method_unwrapDefault
// } from 'virtual:__federation__'

// export async function loadRemote(remoteName, remoteUrl, exposed) {
//    await __federation_method_setRemote(remoteName, {
//         url: `${remoteUrl}/assets/remoteEntry.js`,
//         format: 'esm',
//         from: 'vite',
//         remoteType: 'module' 
//     })
//     const module = await __federation_method_getRemote(remoteName, exposed)
//     return __federation_method_unwrapDefault(module)
// }

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
//   }

import {
  __federation_method_setRemote,
  __federation_method_getRemote,
  __federation_method_unwrapDefault
} from 'virtual:__federation__'

export async function loadRemote(remoteName, remoteUrl, exposedModule) {
  await __federation_method_setRemote(remoteName, {
    url: `${remoteUrl}/assets/remoteEntry.js`,
    format: 'esm',
    from: 'vite',
    remoteType: 'module'
  })

  const mod = await __federation_method_getRemote(remoteName, exposedModule)
  return __federation_method_unwrapDefault(mod)
}