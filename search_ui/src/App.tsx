import { SearchWidget } from './pages/SearchWidget'
import { SearchPage } from './pages/SearchPage'
import { useActions, useAppState } from './AppState'
import { contentTypeLabel, detectSiteLanguage } from './Utils'
import { getProp } from '.'
import { Configuration } from './Interfaces'

export interface AppAttribute {
  name: string
  value: string
}
interface AppProps {
  attrs: AppAttribute[]
  config: Configuration
}
export const App = ({ attrs, config }: AppProps) => {
  const state = useAppState()
  const actions = useActions()

  console.log('attrs', attrs)
  const backendRoot = getProp(attrs, 'data-backend-root') || state.backendRoot
  const accentColor = getProp(attrs, 'data-accent-color') || state.accentColor
  const disableMoreFilters = getProp(attrs, 'data-disable-more-filters') !== null
  actions.setBackendRoot(backendRoot)
  actions.setAccentColor(accentColor)
  actions.setDisableMoreFilters(disableMoreFilters)

  const { contentTypeFilters, languages, language, analytics } = initConfig(config)
  actions.setContentTypeFilters(contentTypeFilters)
  actions.setLanguages(languages)
  actions.setLanguage(language)
  actions.setAnalytics(analytics)

  const instanceId = Math.floor(Math.random() * 1000000) + '-' + new Date().getTime();

  let mode = getProp(attrs, 'data-mode') || 'inline'
  if (['inline', 'widget'].indexOf(mode) === -1) mode = 'inline'

  return (
    <div className={`keha-ui-application keha-ui-application-${mode}`} id={`keha-instance-${instanceId}`}>
      {
        mode === 'widget'
          ? <SearchWidget instanceId={instanceId} />
          : <SearchPage instanceId={instanceId} widget={false} />
      }
    </div>
  )
}

const initConfig = (config: Configuration) => {
  const contentTypeFilters = config.content_types
    .map((id: string) => {
      return {
        id,
        label: contentTypeLabel(id),
        selected: false,
      }
    }).sort((a, b) => {
      return a.label.localeCompare(b.label)
    })
  console.log('content types', contentTypeFilters.map(o => o.id))
  
  let languages = ['fi', 'sv', 'en']
  if (config.languages && config.languages.length > 0) {
    languages = config.languages
  }
  const language = detectSiteLanguage(languages)
  console.log('language [%s] from [%s]', language, languages.join(', '))

  const analytics = config.analytics || {}

  return {
    contentTypeFilters,
    languages,
    language,
    analytics,
  }
}