import { ChangeEvent, KeyboardEvent, FocusEvent, useEffect, useRef, useState } from 'react'
import styled from 'styled-components'
import { useActions, useAppState } from '../AppState'
import { SearchHit } from '../components/molecules/SearchHit'
import { LookingGlassIcon, TrashcanIcon }  from '../assets/Icons'
import { ApiHit, ApiSearchResponse, ContentType, SearchResult } from '../Interfaces'
import { exampleSearchResults, storeKeywordsToSession, getKeywordsFromSession } from '../Utils'
import { executeRequest } from '../BackendAPI'
import { ContentContainer } from '../components/atoms/Containers'
import { SearchTopHeading } from '../components/molecules/SearchTopHeading'
import { SearchResultsFooter } from '../components/molecules/SearchResultsFooter'
import { AllFiltersOverlay } from '../components/organisms/AllFiltersOverlay'
import { FilteringSection } from '../components/organisms/FilteringSection'
import { FilteringSectionSimple } from '../components/organisms/FilteringSectionSimple'
import { FilteringSectionMobile } from '../components/organisms/FilteringSectionMobile'
import { useAnalytics } from '../Analytics'
import { SearchButton } from '../components/atoms/Buttons'

const DimOverlay = styled.div.attrs({className: 'kehauicss-dim-overlay'})<{ visible: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  width: ${p => p.visible ? '100%' : 0};
  height: ${p => p.visible ? '100%' : 0};
  background-color: #000;
  transition: opacity 1s;
  opacity: ${p => p.visible ? 0.1 : 0};
`

const SearchCriteriaContainer = styled.div`
  padding: 0 0 32px;
`

const InputFlex = styled.div`
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
`

const SearchIcon = styled.div<{ top: number, color?: string, hoverColor?: string, onClick?: () => void }>`
  width: 20px;
  height: 20px;
  line-height: 20px;
  font-size: 1.25em;
  position: absolute;
  top: ${p => p.top}px;
  left: 24px;
  color: ${p => p.color ? p.color : 'rgba(0, 0, 0, .8)'};
  cursor: ${p => p.onClick ? 'pointer' : 'default'};
  &:hover {
    color: ${p => p.hoverColor ? p.hoverColor : p.color ? p.color : 'rgba(0, 0, 0, .8)'};
  }
`

const CancelIcon = styled.div<{ top: number, color?: string, hoverColor?: string, onClick?: () => void }>`
  width: 20px;
  height: 20px;
  line-height: 20px;
  font-size: 1.25em;
  position: absolute;
  top: ${p => p.top}px;
  right: 108px;
  color: ${p => p.color ? p.color : 'rgba(0, 0, 0, .8)'};
  cursor: ${p => p.onClick ? 'pointer' : 'default'};
  &:hover {
    color: ${p => p.hoverColor ? p.hoverColor : p.color ? p.color : 'rgba(0, 0, 0, .8)'};
  }
`

const SearchField = styled.input.attrs({className: 'kehauicss-search-field'})`
  font-size: 1em;
  padding: 12px 42px 12px 50px;
  box-sizing: border-box;
  border-radius: 0;
  border: 1px solid rgba(0, 0, 0, .8);
  border-radius: 3px;
  width: 100%;
  &:hover, &:focus {
    outline: 2px solid rgba(0, 0, 0, .8)
  }
`

const SearchResultsContainer = styled.div.attrs({className: 'kehauicss-results'})`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 0 64px;
`

const ResultsHeading = styled.h2.attrs({className: 'kehauicss-resultsheading'})`
  margin: 0 0 48px;
  font-size: 1.75em;
  font-weight: 300;
  span {
    font-family: inherit;
    font-weight: 700;
  }
`

const ErrorMessage = styled.div.attrs({className: 'kehauicss-error-message'})<{ accentColor: string}>`
  color: ${p => p.accentColor};
  font-weight: 700;
`

const SuggestionsBox = styled.div<{ visible?: boolean }>`
  position: relative;
  padding: 8px;
  margin: 0 -8px;
  transition: .4s;
  color: ${p => p.visible ? 'inherit' : 'transparent'};
  background-color: ${p => p.visible ? '#fff' : 'transparent'};
  box-shadow: ${p => p.visible ? '0 4px 16px rgba(0, 0, 0, .25)' : 'none'};
`

const SuggestionRows = styled.div`
  padding: 12px 0;
`

const SuggestionRowElement = styled.div<{ active?: boolean }>`
  position: relative;
  padding: 12px 12px 12px 52px;
  display: flex;
  align-items: center;
  background-color: ${p => p.active ? '#ddd': 'transparent'};
  cursor: pointer;
  &:hover {
    background-color: #ddd;
  }
  a {
    color: inherit;
    text-decoration: none;
    &:hover {
      text-decoration: underline;
    }
  }
`

const SuggestionRowInfo = styled(SuggestionRowElement)`
  color: rgba(0, 0, 0, .5);
  padding: 12px 12px 12px 24px;
  cursor: default;
  font-size: 0.875em;
  &:hover {
    background-color: inherit;
  }
`

const SuggestionText = styled.div`
  padding: 0;
`

interface SearchPageProps {
  instanceId: string
  widget: boolean
  onClose?: () => void
}
export const SearchPage = (props: SearchPageProps) => {
  const PER_PAGE = 10
  const state = useAppState()
  const actions = useActions()
  const [textInputValue, setTextInputValue] = useState(state.keywords)
  const [index, setIndex] = useState(0)
  const [limit, setLimit] = useState(PER_PAGE)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [suggestionsHistoryMode, setSuggestionsHistoryMode] = useState(false)
  const timer = useRef<NodeJS.Timeout | null>(null)
  const [selectedSuggestionIndex, setSelectedSuggestionIndex] = useState(-1)
  const { searchHitToAnalytics } = useAnalytics()
  const allFiltersPanelFocus = useRef<HTMLDivElement>(null)
  const allFiltersButtonFocus = useRef<HTMLDivElement>(null)

  const clearTimer = () => {
    if (timer.current) clearTimeout(timer.current)
    timer.current = null
  }

  useEffect(() => {
    setTextInputValue(state.keywords)
  }, [state.keywords])

  // refresh the search when e.g. filters have been changed
  useEffect(() => {
    if (state.refreshSearch.getTime() === 0) return // skip the refreshing on component mount
    execute()
  }, [state.refreshSearch]) // eslint-disable-line react-hooks/exhaustive-deps

  const fetchSuggestions = async (keywords: string) => {
    const suggestions: string[] = []
    if (!keywords || keywords.trim().length === 0) {
      setSuggestions([])
      return
    }
    const data = {
      search_term: keywords,
      language: state.language,
    }
    const res = await executeRequest(state.backendRoot, 'POST', '/suggest', data)
    if (res.status === 200) {
      const suggest = res.data.suggest || {}
      const values = Object.values(suggest)
      for (const value of values) {
        if (Array.isArray(value) && value.length > 0) {
          const options = value[0].options || []
          if (keywords === 'debug:suggest') {
            options.push({text: 'Lorem'})
            options.push({text: 'Ipsum'})
            options.push({text: 'Dolor'})
          }
          console.log('options', options)
          for (const option of options) {
            suggestions.push(option.text)
          }
        }
      }
      setSuggestionsHistoryMode(false)
      setSuggestions(suggestions.slice(0, 10))
    }
  }

  const startSuggestionsTimer = (keywords: string) => {
    const delay = 100
    const notEmpty = keywords.length > 0
    clearTimer()
    if (notEmpty) {
      timer.current = setTimeout(() => fetchSuggestions(keywords), delay)
    } else {
      setSuggestions([])
    }
  }

  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value

    // TODO hack to change language (until we have a widget for that)
    if (value === 'lang:fi') {
      actions.setLanguage('fi')
    } else if (value === 'lang:sv') {
      actions.setLanguage('sv')
    } else if (value === 'lang:en') {
      actions.setLanguage('en')
    }

    setLimit(PER_PAGE)
    setTextInputValue(value)
    startSuggestionsTimer(value)
    setSelectedSuggestionIndex(-1)
  }

  const onFocus = (e: FocusEvent<HTMLInputElement>) => {
    const value = e.target.value
    if (value) {
      setSuggestionsHistoryMode(false)
      startSuggestionsTimer(value)
    } else {
      const sessionKeywords = getKeywordsFromSession()
      setSuggestionsHistoryMode(true)
      setSuggestions(sessionKeywords)
    }
  }

  const onKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.code === 'Enter') {
      execute(textInputValue)
      e.preventDefault()
    }
    else if (e.code === 'ArrowDown') {
      if (selectedSuggestionIndex < suggestions.length - 1) {
        setSelectedSuggestionIndex(selectedSuggestionIndex + 1)
        setTextInputValue(suggestions[selectedSuggestionIndex + 1])
      }
      e.preventDefault()
    }
    else if (e.code === 'ArrowUp') {
      if (selectedSuggestionIndex > -1) {
        setSelectedSuggestionIndex(selectedSuggestionIndex - 1)
        setTextInputValue(selectedSuggestionIndex > 0 ? suggestions[selectedSuggestionIndex - 1] : '')
      }
      e.preventDefault()
    }
    else if (e.code === 'Escape') {
      setSelectedSuggestionIndex(-1)
      setSuggestions([])
      setSuggestionsHistoryMode(false)
      setTextInputValue('')
      e.preventDefault()
    }
  }

  const cancelKeywords = () => {
    setSelectedSuggestionIndex(-1)
    setSuggestions([])
    setSuggestionsHistoryMode(false)
    setTextInputValue('')
}

  const execute = (keywords?: string) => {
    const trimmed = (keywords || state.keywords).trim() 
    if (trimmed === '') return;

    clearTimer()
    setSuggestions([])
    setSuggestionsHistoryMode(false)
    actions.setKeywords(trimmed)
    actions.setSearching(true)
    actions.setSearchResponse(null)
    fetchResults(index, limit)
    storeKeywordsToSession(keywords)
    searchHitToAnalytics(keywords)
  }

  const loadMore = () => {
    // get currently visible hit elements, and focus on the last one
    const selector = '#keha-instance-' + props.instanceId + ' .kehauicss-result-hit a'
    const hits = document.querySelectorAll(selector)
    if (hits && hits.length > 0) {
      const hit = hits[hits.length - 1] as HTMLElement
      hit.focus()
    }

    fetchResults(index, limit + PER_PAGE)
  }

  const fetchResults = async (index: number, limit: number) => {
    if (state.keywords === 'debug:types') { // for easily testing the different content types
      actions.setSearchResponse({
        results: exampleSearchResults,
        total: exampleSearchResults.length,
        took: 0,
        more: false,
      })
      actions.setSearching(false)
      return
    }

    const filters: any = {}
    if (hasFilters()) {
      filters['content_type'] = state.contentTypeFilters.filter(f => f.selected).map(f => f.id)
    }

    const postData = {
      page_index: index,
      per_page: limit,
      search_term: state.keywords,
      language: state.language,
      filters,
    }
    setIndex(index)
    setLimit(limit)
    try {
      const res = await executeRequest(state.backendRoot, 'POST', '/search', postData)
      if (res.status !== 200) {
        throw new Error('response status ' + res.status)
      }
      const data: ApiSearchResponse = res.data
      
      // combine primary (more relevant) hits with secondary (e.g. partial words)
      const combinedHits = data.primary.hits.concat(data.secondary.hits).slice(0, limit)
      const total = data.primary.metadata.total_count + data.secondary.metadata.total_count
      const took = data.primary.metadata.took + data.secondary.metadata.took
      const more = data.primary.metadata.next_page !== false || data.secondary.metadata.next_page !== false

      // filter out duplicates (same hit might've been in primary and secondary hits)
      const seen = new Set()
      const uniqueHits = combinedHits.filter(hit => {
        const key = hit._id
        return seen.has(key) ? false : seen.add(key)
      })

      if (uniqueHits.length === 0) {
        // TODO if both primary & secondary are empty, make another request with fuzzy search
      }

      // mapping http response data as internal results
      const results: SearchResult[] = uniqueHits.map((hit: ApiHit) => {
        // catenate snippets
        const snippets = hit.highlight || {}
        const snippet = Object.entries(snippets).map(([, value]) => value).join(' … ')
        const imageData = hit.fields.image_url || []
        const image = imageData.length > 0 ? imageData[0] : undefined
        const imageAlt = imageData.length > 1 ? imageData[1] : undefined

        return {
          url: hit.fields.url[0],
          contentType: hit.fields.content_type[0] as ContentType || ContentType.Tietosivu,
          title: hit.fields.title[0] || 'Ei otsikkoa',
          snippet,
          image,
          imageAlt,
          themes: hit.fields.themes || [],
          score: hit._score
        }
      })
      console.debug('axios response as results', results)

      actions.setSearchResponse({
        results,
        total,
        took,
        more,
      })

    } catch (error) {
      actions.setSearchResponse({
        results: [],
        total: 0,
        error: 'Odottamaton hakuvirhe',
        more: false,
      })
    } finally {
      actions.setSearching(false)
    }
  }

  const executeSuggestion = (keywords: string) => {
    console.log('executeSuggestion', { keywords })
    execute(keywords)
  }

  const SuggestionRow = ({ text, index }: { text: string, index: number }) => {
    if (!text || text.trim().length === 0) return null
    return (
      <SuggestionRowElement aria-label={text} active={index === selectedSuggestionIndex} onClick={() => executeSuggestion(text)}>
        <SearchIcon top={12}><LookingGlassIcon /></SearchIcon>
        <SuggestionText>{text}</SuggestionText>
      </SuggestionRowElement>
    )
  }

  const hasFilters = () => {
    for (const option of state.contentTypeFilters) {
      if (option.selected) return true
    }
    return false
  }

  const dimOverlayClicked = () => {
    if (state.allFiltersOpen) {
      actions.setAllFiltersOpen(false)
    } else if (suggestions.length > 0) {
      setSelectedSuggestionIndex(-1)
      setSuggestions([])
      setSuggestionsHistoryMode(false)
    }
  }

  const simple = true // TODO after support for multiple filters, use simple only when there is just a single filter group
  const res = state.searchResponse
  return (
    <>
      <DimOverlay
        visible={suggestions.length > 0 || state.allFiltersOpen}
        onClick={dimOverlayClicked} />

      <div className='back-to-top'></div>
      <ContentContainer widget={props.widget} role='search'>

        <SearchTopHeading widget={props.widget} onClose={props.onClose} />
        
        <SearchCriteriaContainer className='searchCriteriaContainer'>
          <SuggestionsBox visible={suggestions.length > 0} >
            <InputFlex>
              <SearchIcon top={14} color={state.accentColor}>
                <LookingGlassIcon />
              </SearchIcon>
              <SearchField id={`keha-search-field-${props.instanceId}`} type='text' role='combobox' aria-expanded={suggestions.length > 0} aria-autocomplete='both' aria-haspopup='false' autoCapitalize='off' autoCorrect='off' spellCheck={false} aria-label='Hakukenttä' placeholder={`Kirjoita hakusana…`} autoComplete='off' value={textInputValue} onChange={onChange} onKeyDown={onKeyDown} onFocus={onFocus} />
              {textInputValue &&
                <CancelIcon top={13} hoverColor={state.accentColor} tabIndex={0} role='button' aria-label='Tyhjennä hakukenttä' onKeyPress={cancelKeywords} onClick={cancelKeywords} >
                  <TrashcanIcon />
                </CancelIcon>
              }
              <SearchButton type='submit' accentColor={state.accentColor} onClick={() => execute(textInputValue)} disabled={state.searching}>
                Hae <LookingGlassIcon />
              </SearchButton>
            </InputFlex>
            <SuggestionRows>
              {suggestionsHistoryMode && <SuggestionRowInfo>Viimeksi hakemasi</SuggestionRowInfo>}
              {suggestions.map((text, i) => <SuggestionRow key={text} text={text} index={i} />)}
            </SuggestionRows>
          </SuggestionsBox>
        </SearchCriteriaContainer>

        {res !== null &&
          <ResultsHeading aria-live='polite'>
            {hasFilters() ?
              <>
                {res.total} suodatettua tulosta
              </> :
              <>
                {res.total} hakutulosta sanalla <span><span aria-hidden>“</span>{state.keywords}<span aria-hidden>”</span></span>
              </>
            }
          </ResultsHeading>
        }

      </ContentContainer>

      {res !== null && 
        <div onFocus={dimOverlayClicked}>
          { simple ?
            <FilteringSectionSimple widget={props.widget} allFiltersPanelFocus={allFiltersPanelFocus} allFiltersButtonFocus={allFiltersButtonFocus} /> :
            <FilteringSection widget={props.widget} allFiltersPanelFocus={allFiltersPanelFocus} allFiltersButtonFocus={allFiltersButtonFocus} />
          }
          <FilteringSectionMobile widget={props.widget} allFiltersPanelFocus={allFiltersPanelFocus} allFiltersButtonFocus={allFiltersButtonFocus} />
        </div>
      }

      <AllFiltersOverlay
        visible={state.allFiltersOpen}
        close={() => actions.setAllFiltersOpen(false)}
        allFiltersPanelFocus={allFiltersPanelFocus}
        allFiltersButtonFocus={allFiltersButtonFocus} />

      {res !== null && 
        <>
          <SearchResultsContainer onFocus={dimOverlayClicked}>
            <ContentContainer widget={props.widget} aria-live='polite' role='list'>

              { res.results.map(result =>
                <SearchHit key={result.url} result={result} />)
              }

              { res.results.length > 0 &&
                <SearchResultsFooter instanceId={props.instanceId} more={res.more} onShowMore={loadMore} />
              }

              { res.error &&
                <ErrorMessage accentColor={state.accentColor}>{res.error}, yritä myöhemmin uudestaan.</ErrorMessage>
              }

            </ContentContainer>
          </SearchResultsContainer>
        </>
      }

    </>
  )
}
