export interface ApiSearchResponse {
  primary: ApiSearchResponseContainer
  secondary: ApiSearchResponseContainer
}

export interface ApiSearchResponseContainer {
  hits: ApiHit[]
  metadata: ApiMetadata
}

export interface ApiHit {
  _id: string
  _index: string
  _score: number
  _type: '_doc'
  fields: ApiHitFields
  highlight: any
}

export interface ApiHitFields {
  url: string[] // TODO why array?
  title: string[] // TODO why array?
  text: string[] // TODO why array?
  image_url: string[] // TODO why array?
  content_type: string[] // TODO why array?
  keywords: string[] // TODO array not contents is single element with comma separated words
  themes: string[]
}

export interface ApiMetadata {
  page_index: number // requested page index
  per_page: number // requested page limit
  next_page: number | boolean // index of the start of next page (if more results), false if no more results
  previous_page: number | boolean // index of start of the previous page, false if no previous page available
  first_page: number // index of the first page (always 0 apparently)
  last_page: number // index of the last page
  page_count: number // number of total pages
  took: number // query execution time in milliseconds
  total_count: number // number of total hits
}

export interface SearchResponse {
  results: SearchResult[]
  more: boolean // more results availble? i.e. shall we show the "load more" button
  total: number
  error?: string
  took?: number // query time in milliseconds
}

export interface SearchResult {
  url: string
  contentType: ContentType
  title: string
  themes: string[]
  snippet: string
  score: number
  date?: Date
  place?: string // event location or street address
  phone?: string
  author?: string // author (name) of the news, blog, article or similar
  image?: string // image url of the content (any type)
  imageAlt?: string
}

export enum ContentType {
  Tietosivu = 'tietosivu',
  Uutinen = 'uutinen',
  Blogi = 'blogi',
  Yhteystieto = 'yhteystieto',
  Tapahtuma = 'tapahtuma',
  Palvelu = 'palvelu_tai_asiointikanava',
  Toimipaikka = 'toimipaikka',
}

export interface Filter {
  id: string
  label: string
}

export const contentTypeFilter: Filter = {
  id: 'contentType',
  label: 'Sisältötyyppi',
}

export interface FilterOption {
  id: string
  label: string
  selected: boolean
}

export interface Configuration {
  analytics: ConfigurationAnalytics
  content_types: string[]
  languages: any
}

export interface ConfigurationAnalytics {
  google_analytics_id?: string
  google_tag_manager_id?: string
  matomo?: MatomoAnalytics
}

interface MatomoAnalytics {
  base_url?: string
  site_id?: number
}