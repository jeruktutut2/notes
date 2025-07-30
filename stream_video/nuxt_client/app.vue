<template>
    <div>
        <!-- <NuxtRouteAnnouncer /> -->
        <!-- <NuxtWelcome /> -->
        <div class="video-player">
          <video :src="'/file/stream-video'" controls preload="metadata" class="w-full max-w-2xl rounded-lg shadow" />
        </div>
    </div>
</template>
