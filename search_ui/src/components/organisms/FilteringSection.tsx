import { RefObject } from 'react'
import styled from 'styled-components'
import { Breakpoint } from '../../Constants'
import { useActions, useAppState } from '../../AppState'
import { ContentContainer, FlexContentContainer, HideMobile } from '../atoms/Containers'
import { FilterElement, FilterGroup } from '../organisms/FilterGroup'
import { CloseFilterIcon, SlidersIcon }  from '../../assets/Icons'
import { contentTypeFilter, FilterOption } from '../../Interfaces'
import { onKeyEnter } from '../../Utils'

export const FilterDivider = styled.div`
  margin-top: 16px;
  margin-bottom: 48px;
  display: flex;
  align-items: center;
  & > *:first-child {
    margin-right: 16px;
    margin-left: -16px;
  }
`

export const FilterContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 8px;

  @media (max-width: ${Breakpoint.Small}) {
    flex-direction: column;
    align-items: center;
  }
`

export const FilterLabel = styled.div`
  padding: 0 0 16px 0;
  font-weight: 700;
`

export const SeparatorLine = styled.div<{ flex: number }>`
  flex: ${p => p.flex};
  height: 0px;
  border-top: 1px solid rgba(0, 0, 0, .8);
`

const ActiveFilters = styled.div`
  margin: 32px 0 16px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;

  @media (max-width: ${Breakpoint.Small}) {
    justify-content: center;
  }
`

interface FilteringSectionProps {
  widget: boolean
  allFiltersPanelFocus: RefObject<HTMLDivElement>
  allFiltersButtonFocus: RefObject<HTMLDivElement>
}
export const FilteringSection = (props: FilteringSectionProps) => {
  const state = useAppState()
  const actions = useActions()
  const res = state.searchResponse
  const hasResults = res && res.results?.length > 0

  const hasFilters = () => {
    for (const option of state.contentTypeFilters) {
      if (option.selected) return true
    }
    return false
  }

  const listOfSelectedFilterOptions = () => {
    const list: FilterOption[] = []
    for (const option of state.contentTypeFilters) {
      if (option.selected) {
        list.push(option)
      }
    }
    return list
  }

  const unselectFilter = (filterId: string, optionId: string) => {
    console.log('unselectFilter', {filterId, optionId})

    if (filterId === 'contentType') {
      const newOptions = []
      for (const option of state.contentTypeFilters) {
        const newOption = {...option}
        if (newOption.id === optionId || optionId === '*') {
          newOption.selected = false
        }
        newOptions.push(newOption)
      }
      actions.setContentTypeFilters(newOptions)
    }
    actions.setRefreshSearch()
  }

  const openAllFilters = () => {
    actions.setAllFiltersOpen(true)
    if (props.allFiltersPanelFocus?.current) (
      props.allFiltersPanelFocus.current.focus()
    )
  }

  return (
    <HideMobile>
      { (hasResults || hasFilters()) &&
        <>
          <ContentContainer widget={props.widget}>
            <FilterLabel>Suodata hakutuloksia:</FilterLabel>
          </ContentContainer>
          <FilterDivider>
            <SeparatorLine flex={props.widget ? 1 : 0} />
            <FlexContentContainer widget={props.widget}>
              <FilterContainer>
                <FilterGroup
                  filter={contentTypeFilter}
                  options={state.contentTypeFilters}
                  />
                <FilterElement ref={props.allFiltersButtonFocus} tabIndex={0} accentColor={state.accentColor} role='button' open={state.allFiltersOpen} onClick={openAllFilters} onKeyPress={e => onKeyEnter(e, openAllFilters)}>
                  Kaikki suodattimet <SlidersIcon />
                </FilterElement>
              </FilterContainer>
              <SeparatorLine flex={1} style={{ marginLeft: '16px' }}/>
            </FlexContentContainer>
            <SeparatorLine flex={1} />
          </FilterDivider>
        </>
      }

      {hasFilters() &&
        <ContentContainer widget={props.widget}>
          <ActiveFilters>
              <>
                {listOfSelectedFilterOptions().map(option => (
                  <FilterElement tabIndex={0} key={'content-type-' + option.id} role='button' accentColor={state.accentColor}
                    onKeyPress={e => onKeyEnter(e, () => unselectFilter('contentType', option.id))}
                    onClick={() => unselectFilter('contentType', option.id)} selected>
                    {option.label} <CloseFilterIcon />
                  </FilterElement>
                ))}
                <FilterElement tabIndex={0} role='button' accentColor={state.accentColor}
                  onKeyPress={e => onKeyEnter(e, () => unselectFilter('contentType', '*'))}
                  onClick={() => unselectFilter('contentType', '*')}>
                  Poista kaikki <CloseFilterIcon />
                </FilterElement>
              </>
          </ActiveFilters>
        </ContentContainer>
      }
    </HideMobile>
  )
}