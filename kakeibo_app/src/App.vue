<template>
  <div class="app">
    <aside v-if="!isMobile" class="sidebar">
      <h1 class="sidebar-title">家計簿</h1>
      <nav>
        <router-link v-for="tab in tabs" :key="tab.path" :to="tab.path" class="sidebar-link">
          <span class="tab-icon">{{ tab.icon }}</span>
          <span>{{ tab.label }}</span>
        </router-link>
      </nav>
    </aside>

    <main class="main-content">
      <router-view />
    </main>

    <nav v-if="isMobile" class="tab-bar">
      <router-link v-for="tab in mobileTabs" :key="tab.path" :to="tab.path" class="tab-item">
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-label">{{ tab.label }}</span>
      </router-link>
    </nav>

    <ToastHost />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import ToastHost from './components/ToastHost.vue'
import ConfirmDialog from './components/ConfirmDialog.vue'

const tabs = [
  { path: '/monthly', icon: '📅', label: '月の支出' },
  { path: '/weekly', icon: '📆', label: '週の支出' },
  { path: '/annual', icon: '🗓️', label: '年間' },
  { path: '/income', icon: '💵', label: '収入・収支' },
  { path: '/budget', icon: '💰', label: '予算' },
  { path: '/work', icon: '⏰', label: 'バイト' },
  { path: '/debt', icon: '📋', label: '借金' },
  { path: '/analysis', icon: '📊', label: '分析' },
  { path: '/import', icon: '📥', label: '取込' },
  { path: '/settings', icon: '⚙️', label: '設定' },
]

const mobileTabs = computed(() => tabs.slice(0, 8))

const isMobile = ref(window.innerWidth <= 768)

function onResize() {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => window.addEventListener('resize', onResize))
onUnmounted(() => window.removeEventListener('resize', onResize))
</script>
