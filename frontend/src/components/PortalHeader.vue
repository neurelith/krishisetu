<template>
  <header class="portal-header sky sky-strip" :data-risk="risk">
    <div class="portal-header-inner">
      <div class="portal-header-main">
        <div class="portal-header-icon" aria-hidden="true">
          <component :is="icon" :size="25" weight="bold" />
        </div>
        <div class="portal-header-copy">
          <div class="portal-header-title-row">
            <h1>{{ title }}</h1>
            <span v-if="badge" class="badge-institutional badge-sky portal-header-badge">{{ badge }}</span>
            <slot name="meta" />
          </div>
          <p class="portal-header-status">{{ subtitle }}</p>
        </div>
      </div>
      <div v-if="$slots.actions" class="portal-header-actions">
        <slot name="actions" />
      </div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, required: true },
  icon: { type: [Object, Function], required: true },
  risk: { type: String, default: 'clear' },
  badge: { type: String, default: '' }
})
</script>

<style scoped>
.portal-header {
  padding: 32px 24px 84px;
  color: var(--color-cloud-white);
}

.portal-header-inner {
  width: min(100%, var(--page-max-width));
  margin: 0 auto;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}

.portal-header-main {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  min-width: 0;
}

.portal-header-icon {
  width: 52px;
  height: 52px;
  flex: 0 0 52px;
  display: grid;
  place-items: center;
  border: 1px solid var(--color-haze);
  border-radius: 16px;
  color: var(--color-cloud-white);
  background: var(--color-storm);
}

.portal-header-copy {
  min-width: 0;
}

.portal-header-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.portal-header-title-row h1 {
  margin: 0;
  color: var(--color-cloud-white);
  font-family: var(--font-display);
  font-size: clamp(36px, 5vw, 54px);
  font-weight: 300;
  letter-spacing: -0.025em;
  line-height: 1.08;
}

.portal-header-badge {
  border-color: var(--color-haze);
  background: transparent;
  color: var(--color-cloud-white);
}

.portal-header-status {
  max-width: 70ch;
  margin: 10px 0 0;
  color: var(--color-cloud-white);
  font-size: var(--text-body);
  line-height: 1.5;
}

.portal-header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

@media (max-width: 640px) {
  .portal-header {
    padding: 24px 16px 72px;
  }

  .portal-header-inner {
    align-items: stretch;
  }

  .portal-header-main {
    gap: 12px;
  }

  .portal-header-icon {
    width: 44px;
    height: 44px;
    flex-basis: 44px;
  }

  .portal-header-title-row h1 {
    font-size: 38px;
  }

  .portal-header-actions {
    width: 100%;
  }

  .portal-header-actions > * {
    width: 100%;
  }
}
</style>
