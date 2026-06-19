<template>
  <div>
    <div class="month-nav">
      <button @click="changeMonth(-1)">&lt;</button>
      <span>{{ displayMonth }}</span>
      <button @click="changeMonth(1)">&gt;</button>
    </div>

    <!-- バイト先管理 -->
    <div class="card">
      <h2 class="page-title">バイト先</h2>
      <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.75rem">
        <span
          v-for="job in jobs"
          :key="job.job_id"
          class="category-pill"
          :class="{ active: selectedJob?.job_id === job.job_id }"
          style="display: inline-flex; align-items: center; gap: 0.2rem"
        >
          <button class="job-pill-name" @click="selectJob(job)">{{ job.store_name }}</button>
          <button class="job-pill-icon" style="color: var(--primary)" @click="startEditJob(job)">✎</button>
          <button class="job-pill-icon" style="color: var(--danger)" @click="removeJob(job)">✕</button>
        </span>
        <button class="category-pill" style="border-style: dashed" @click="openAddJob">＋ 新規</button>
      </div>

      <div v-if="showJobForm" class="card" style="background: #f8f9fa">
        <h3 style="font-size: 0.95rem; font-weight: 600; margin-bottom: 0.5rem">
          {{ editingJobId ? 'バイト先を編集' : '新しいバイト先' }}
        </h3>
        <div class="form-group">
          <label>店名・会社名</label>
          <input type="text" v-model="jobForm.storeName" placeholder="例: コンビニA店" />
        </div>
        <div style="display: flex; gap: 0.5rem">
          <div class="form-group" style="flex: 1">
            <label>時給（円）</label>
            <input type="number" v-model.number="jobForm.hourlyRate" inputmode="numeric" placeholder="1200" />
          </div>
          <div class="form-group" style="flex: 1">
            <label>日給（円・任意）</label>
            <input type="number" v-model.number="jobForm.dailyRate" inputmode="numeric" placeholder="0" />
          </div>
        </div>
        <div class="form-group">
          <label>交通費（円/日）</label>
          <input type="number" v-model.number="jobForm.transportCost" inputmode="numeric" placeholder="0" />
        </div>
        <div style="display: flex; gap: 0.5rem">
          <button class="btn btn-primary btn-sm" @click="submitJob">{{ editingJobId ? '更新' : '登録' }}</button>
          <button class="btn btn-sm" style="background: var(--border)" @click="closeJobForm">取消</button>
        </div>
      </div>

      <div v-if="selectedJob" style="font-size: 0.8rem; color: var(--text-muted); padding: 0.25rem 0">
        {{ selectedJob.store_name }} — 時給: {{ Number(selectedJob.hourly_rate).toLocaleString() }}円
        <span v-if="Number(selectedJob.transport_cost)">／交通費: {{ Number(selectedJob.transport_cost).toLocaleString() }}円</span>
      </div>
    </div>

    <!-- 勤怠入力 -->
    <div class="card">
      <h2 class="page-title">勤怠入力</h2>
      <div class="form-group">
        <label>日付</label>
        <input type="date" v-model="form.dateStr" />
      </div>
      <div style="display: flex; gap: 0.5rem">
        <div class="form-group" style="flex: 1">
          <label>開始</label>
          <input type="time" v-model="form.startTime" />
        </div>
        <div class="form-group" style="flex: 1">
          <label>終了</label>
          <input type="time" v-model="form.endTime" />
        </div>
      </div>
      <div class="form-group">
        <label>休憩（分）</label>
        <input type="number" v-model.number="form.breakMinutes" inputmode="numeric" />
      </div>
      <div v-if="calcHours > 0" style="margin-bottom: 0.75rem; font-size: 0.9rem; color: var(--text-muted)">
        実働 {{ calcHours.toFixed(1) }}h → {{ calcPay.toLocaleString() }}円
        <span v-if="calcTransport > 0">＋ 交通費{{ calcTransport.toLocaleString() }}円</span>
      </div>
      <button class="btn btn-primary btn-block" @click="submitWork" :disabled="!selectedJob">
        {{ selectedJob ? '保存' : 'バイト先を選択してください' }}
      </button>
    </div>

    <!-- 月間集計 -->
    <div class="card">
      <div class="summary-row total">
        <span>月間合計勤務</span>
        <span>{{ totalHours.toFixed(1) }}h</span>
      </div>
      <div class="summary-row total">
        <span>見込み給与</span>
        <span>{{ totalPay.toLocaleString() }}円</span>
      </div>
      <div v-if="totalTransport > 0" class="summary-row">
        <span>交通費合計</span>
        <span>{{ totalTransport.toLocaleString() }}円</span>
      </div>
      <div v-if="jobBreakdown.length > 1" style="margin-top: 0.5rem; border-top: 1px solid var(--border); padding-top: 0.5rem">
        <div v-for="jb in jobBreakdown" :key="jb.name" class="summary-row">
          <span>{{ jb.name }}</span>
          <span>{{ jb.pay.toLocaleString() }}円 ({{ jb.hours.toFixed(1) }}h)</span>
        </div>
      </div>
    </div>

    <!-- 勤務一覧 -->
    <div class="card">
      <h2 class="page-title">勤務一覧</h2>
      <div v-if="!workLogs.length" class="empty-state">勤務データがありません</div>
      <ul v-else class="expense-list">
        <li v-for="w in workLogs" :key="w.work_id" class="expense-item">
          <div class="expense-info">
            <div class="expense-name">{{ w.date_str }} <span v-if="w.job_name" style="color: var(--primary); font-size: 0.8rem">{{ w.job_name }}</span></div>
            <div class="expense-meta">{{ w.start_time }} - {{ w.end_time }} (休{{ w.break_minutes }}分)</div>
          </div>
          <div style="text-align: right">
            <div class="expense-amount">{{ Number(w.daily_pay).toLocaleString() }}円</div>
            <div class="expense-meta">
              {{ Number(w.work_hours).toFixed(1) }}h
              <span v-if="Number(w.transport_cost)">+交{{ Number(w.transport_cost).toLocaleString() }}</span>
            </div>
          </div>
          <button class="btn btn-danger btn-sm" @click="removeWork(w.work_id)">削除</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { getWorkLog, saveWorkLog, deleteWorkLog, getJobs, saveJob, deleteJob, isConfigured } from '../services/sheets-api'

const today = new Date()
const currentYM = ref(`${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`)
const workLogs = ref([])
const jobs = ref([])
const selectedJob = ref(null)
const showJobForm = ref(false)
const editingJobId = ref('')
const jobForm = ref({ storeName: '', hourlyRate: '', dailyRate: '', transportCost: 0 })

const form = ref({
  dateStr: today.toISOString().slice(0, 10),
  startTime: '09:00',
  endTime: '17:00',
  breakMinutes: 60,
})

const displayMonth = computed(() => {
  const [y, m] = currentYM.value.split('-')
  return `${y}年${parseInt(m)}月`
})

const calcHours = computed(() => {
  const [sh, sm] = (form.value.startTime || '0:0').split(':').map(Number)
  const [eh, em] = (form.value.endTime || '0:0').split(':').map(Number)
  const mins = (eh * 60 + em) - (sh * 60 + sm) - (form.value.breakMinutes || 0)
  return Math.max(0, mins / 60)
})

const calcPay = computed(() => {
  if (!selectedJob.value) return 0
  return Math.round(calcHours.value * Number(selectedJob.value.hourly_rate))
})

const calcTransport = computed(() => Number(selectedJob.value?.transport_cost || 0))

const totalHours = computed(() => workLogs.value.reduce((s, w) => s + Number(w.work_hours), 0))
const totalPay = computed(() => workLogs.value.reduce((s, w) => s + Number(w.daily_pay), 0))
const totalTransport = computed(() => workLogs.value.reduce((s, w) => s + Number(w.transport_cost || 0), 0))

const jobBreakdown = computed(() => {
  const map = {}
  for (const w of workLogs.value) {
    const name = w.job_name || '不明'
    if (!map[name]) map[name] = { name, hours: 0, pay: 0 }
    map[name].hours += Number(w.work_hours)
    map[name].pay += Number(w.daily_pay)
  }
  return Object.values(map)
})

function selectJob(job) {
  selectedJob.value = job
}

function changeMonth(delta) {
  const [y, m] = currentYM.value.split('-').map(Number)
  const d = new Date(y, m - 1 + delta, 1)
  currentYM.value = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
}

async function fetchData() {
  if (!isConfigured()) return
  try {
    workLogs.value = await getWorkLog(currentYM.value)
    jobs.value = await getJobs()
    if (jobs.value.length && !selectedJob.value) {
      selectedJob.value = jobs.value[0]
    }
  } catch (e) {
    console.error('Failed to fetch work data:', e)
  }
}

function openAddJob() {
  editingJobId.value = ''
  jobForm.value = { storeName: '', hourlyRate: '', dailyRate: '', transportCost: 0 }
  showJobForm.value = true
}

function startEditJob(job) {
  editingJobId.value = job.job_id
  jobForm.value = {
    storeName: job.store_name,
    hourlyRate: Number(job.hourly_rate || 0),
    dailyRate: Number(job.daily_rate || 0),
    transportCost: Number(job.transport_cost || 0),
  }
  showJobForm.value = true
}

function closeJobForm() {
  showJobForm.value = false
  editingJobId.value = ''
}

async function submitJob() {
  if (!jobForm.value.storeName || !jobForm.value.hourlyRate) return
  try {
    const payload = { ...jobForm.value }
    if (editingJobId.value) payload.id = editingJobId.value
    await saveJob(payload)
    closeJobForm()
    jobForm.value = { storeName: '', hourlyRate: '', dailyRate: '', transportCost: 0 }
    await fetchData()
  } catch (e) {
    console.error('Failed to save job:', e)
    alert((editingJobId.value ? '更新' : '登録') + 'に失敗しました: ' + e.message)
  }
}

async function removeJob(job) {
  if (!confirm(`バイト先「${job.store_name}」を削除しますか？\n過去の勤怠データがある場合はスプレッドシートに残り、「削除された項目です」として記載されます。`)) return
  try {
    await deleteJob(job.job_id)
    if (selectedJob.value?.job_id === job.job_id) selectedJob.value = null
    await fetchData()
  } catch (e) {
    console.error('Failed to delete job:', e)
    alert('削除に失敗しました: ' + e.message)
  }
}

async function submitWork() {
  if (!selectedJob.value) return
  try {
    await saveWorkLog({
      dateStr: form.value.dateStr,
      startTime: form.value.startTime,
      endTime: form.value.endTime,
      breakMinutes: form.value.breakMinutes,
      hourlyRate: Number(selectedJob.value.hourly_rate),
      jobName: selectedJob.value.store_name,
      transportCost: Number(selectedJob.value.transport_cost || 0),
    })
    await fetchData()
  } catch (e) {
    console.error('Failed to save work log:', e)
    alert('保存に失敗しました: ' + e.message)
  }
}

async function removeWork(id) {
  if (!confirm('削除しますか？')) return
  try {
    await deleteWorkLog(id)
    await fetchData()
  } catch (e) {
    console.error('Failed to delete:', e)
  }
}

watch(currentYM, fetchData)
onMounted(fetchData)
</script>

<style scoped>
.job-pill-name {
  background: none;
  border: none;
  cursor: pointer;
  font: inherit;
  color: inherit;
  padding: 0;
}
.job-pill-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.8rem;
  padding: 0;
  line-height: 1;
}
</style>
