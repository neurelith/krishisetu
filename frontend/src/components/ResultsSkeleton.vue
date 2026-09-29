<template>
  <div class="results-skeleton" aria-hidden="true">
    <div class="score-band">
      <div v-for="n in 4" :key="n" class="score-card skeleton-card">
        <Skeleton width="60%" height="10px" />
        <Skeleton width="40%" height="28px" />
        <Skeleton width="70%" height="10px" />
      </div>
    </div>
    <div class="panel">
      <Skeleton width="40%" height="16px" />
      <Skeleton width="100%" height="80px" />
    </div>
    <div class="panel">
      <Skeleton width="30%" height="16px" />
      <Skeleton width="100%" height="120px" />
    </div>
  </div>
</template>

<script setup>
import Skeleton from './Skeleton.vue'
</script>
