import styled from 'styled-components'
import { useActions, useAppState } from '../../AppState'
import { FlexContentContainer, HideMobile } from '../atoms/Containers'
import { FilterElement } from '../organisms/FilterGroup'
import { CheckMarkIcon, SlidersIcon }  from '../../assets/Icons'
import { FilterDivider, SeparatorLine, FilterContainer } from './FilteringSection'
import { onKeyEnter } from '../../Utils'
import { RefObject } from 'react'

interface FilteringSectionSimpleProps {
  widget: boolean
  allFiltersPanelFocus: RefObject<HTMLDivElement>
  allFiltersButtonFocus: RefObject<HTMLDivElement>
}
export const FilteringSectionSimple = (props: FilteringSectionSimpleProps) => {
  const state = useAppState()
  const actions = useActions()

  const toggleFilter = (filterId: string, optionId: string) => {
    console.log('toggleFilter', {filterId, optionId})

    if (filterId === 'contentType') {
      const newOptions = []
      for (const option of state.contentTypeFilters) {
        const newOption = {...option}
        if (newOption.id === optionId) {
          newOption.selected = !newOption.selected
        }
        newOptions.push(newOption)
      }
      actions.setContentTypeFilters(newOptions)
    }
    actions.setRefreshSearch()
  }

  const openAllFilters = () => {
    actions.setAllFiltersOpen(true)
    if (props.allFiltersPanelFocus?.current) {
      props.allFiltersPanelFocus.current.focus()
    }
  }

  const showAllActive = () => {
    const selectedFilters = state.contentTypeFilters.filter(f => f.selected)
    return selectedFilters.length === 0
  }

  const showAll = () => {
    const newOptions = state.contentTypeFilters.map(option => {
      const newOption = {...option}
      newOption.selected = false
      return newOption
    })
    actions.setContentTypeFilters(newOptions)
    actions.setRefreshSearch()
  }

  return (
    <HideMobile>
      <FilterDivider>
        <SeparatorLine flex={props.widget ? 1 : 0} />
        <FlexContentContainer widget={props.widget} style={{ width: 'auto' }}>
          <FilterContainer>
            <FilterElement tabIndex={0} role='button' accentColor={state.accentColor} selected={showAllActive()} onClick={showAll} onKeyPress={e => onKeyEnter(e, showAll)}>
              <CheckMark color='white' selected={showAllActive()}>
                <CheckMarkIcon />
              </CheckMark>
              Näytä kaikki
            </FilterElement>
            {state.contentTypeFilters.map(option => (
              <FilterElement tabIndex={0} key={'content-type-' + option.id} accentColor={state.accentColor}
                onClick={() => toggleFilter('contentType', option.id)} selected={option.selected}
                role='checkbox' onKeyPress={e => onKeyEnter(e, () => toggleFilter('contentType', option.id))} aria-checked={option.selected}>
                <CheckMark color='white' selected={option.selected}>
                  <CheckMarkIcon />
                </CheckMark>
                {option.label}
                <Number aria-hidden='true'>123</Number>{ /* TODO implement when support for content type counts is done on backend */ }
              </FilterElement>
            ))}
            {!state.disableMoreFilters &&
            <FilterElement ref={props.allFiltersButtonFocus} tabIndex={0} role='button' accentColor={state.accentColor} open={state.allFiltersOpen} onClick={openAllFilters} onKeyPress={e => onKeyEnter(e, openAllFilters)}>
              Lisää suodattimia <SlidersIcon />
            </FilterElement>}
          </FilterContainer>
          <SeparatorLine flex={1} style={{ marginLeft: '16px' }}/>
        </FlexContentContainer>
        <SeparatorLine flex={1} />
      </FilterDivider>
    </HideMobile>
  )
}

const CheckMark = styled.div<{ color: string, selected: boolean }>`
  color: ${p => p.color};
  margin-right: 4px;
  display: ${p => p.selected ? 'block' : 'none'};
`

const Number = styled.div`
  color: rgba(0, 0, 0, .5);
  margin-left: 4px;
  display: none; // TODO display when support for content type counts is done on backend
`