import { createOvermind, IContext } from 'overmind'
import { createStateHook, createActionsHook } from 'overmind-react'
import { ConfigurationAnalytics, FilterOption, SearchResponse } from './Interfaces'

export type State = {
  backendRoot: string
  keywords: string
  searching: boolean
  searchResponse: SearchResponse | null
  languages: string[]
  language: string
  contentTypeFilters: FilterOption[]
  contentTypeFiltersOpen: boolean
  allFiltersOpen: boolean
  refreshSearch: Date
  accentColor: string
  analytics: ConfigurationAnalytics
  disableMoreFilters: boolean
}
const state: State = {
  backendRoot: 'http://localhost:5000',
  keywords: '',
  searching: false,
  searchResponse: null,
  languages: [],
  language: '',
  contentTypeFilters: [],
  contentTypeFiltersOpen: false,
  allFiltersOpen: false,
  refreshSearch: new Date(0),
  accentColor: '#C82A07',
  analytics: {},
  disableMoreFilters: false,
}

export type Actions = {
  onInitializeOvermind: (c: Context) => void
  setBackendRoot: (c: Context, s: string) => void
  setKeywords: (c: Context, s: string) => void
  setSearching: (c: Context, b: boolean) => void
  setSearchResponse: (c: Context, r: SearchResponse | null) => void
  setLanguages: (c: Context, l: string[]) => void
  setLanguage: (c: Context, l: string) => void
  setContentTypeFilters: (c: Context, f: FilterOption[]) => void
  setContentTypeFiltersOpen: (c: Context, b: boolean) => void
  setAllFiltersOpen: (c: Context, b: boolean) => void
  setRefreshSearch: (c: Context) => void
  setAccentColor: (c: Context, s: string) => void
  setAnalytics: (c: Context, a: ConfigurationAnalytics) => void
  setDisableMoreFilters: (c: Context, b: boolean) => void
}
const actions: Actions = {
  onInitializeOvermind: () => {
    console.log('### overmind init done')
  },
  setBackendRoot: (c: Context, s: string) => {
    c.state.backendRoot = s
  },
  setKeywords: (c: Context, s: string) => {
    c.state.keywords = s
  },
  setSearching: (c: Context, b: boolean) => {
    c.state.searching = b
  },
  setSearchResponse: (c: Context, r: SearchResponse | null) => {
    c.state.searchResponse = r
  },
  setLanguages: (c: Context, l: string[]) => {
    c.state.languages = l
  },
  setLanguage: (c: Context, l: string) => {
    c.state.language = l
  },
  setContentTypeFilters: (c: Context, o: FilterOption[]) => {
    c.state.contentTypeFilters = o
  },
  setContentTypeFiltersOpen: (c: Context, b: boolean) => {
    c.state.contentTypeFiltersOpen = b
  },
  setAllFiltersOpen: (c: Context, b: boolean) => {
    c.state.allFiltersOpen = b
  },
  setRefreshSearch: (c: Context) => (
    c.state.refreshSearch = new Date()
  ),
  setAccentColor: (c: Context, s: string) => {
    c.state.accentColor = s
  },
  setAnalytics: (c: Context, a: ConfigurationAnalytics) => {
    c.state.analytics = a
  },
  setDisableMoreFilters: (c: Context, b: boolean) => {
    c.state.disableMoreFilters = b
  },
}

type Effects = {}
const effects: Effects = {}

export type Context = IContext<{
  state: State
  actions: Actions
  effects: Effects
}>

export const overmind = createOvermind({ state, actions, effects }, { devtools: false })
export const useAppState = createStateHook<Context>()
export const useActions = createActionsHook<Context>()
