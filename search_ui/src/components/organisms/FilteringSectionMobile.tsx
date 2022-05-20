import styled from 'styled-components'
import { useActions, useAppState } from '../../AppState'
import { OnlyMobile } from '../atoms/Containers'
import { FilterElement } from '../organisms/FilterGroup'
import { ChevronDownIcon, SlidersIcon, ThinCloseIcon }  from '../../assets/Icons'
import { FilterContainer } from './FilteringSection'
import { onKeyEnter } from '../../Utils'
import { RefObject } from 'react'

interface FilteringSectionMobileProps {
  widget: boolean
  allFiltersPanelFocus: RefObject<HTMLDivElement>
  allFiltersButtonFocus: RefObject<HTMLDivElement>
}
export const FilteringSectionMobile = (props: FilteringSectionMobileProps) => {
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

  const hasSelectedFilters = () => {
    const selectedFilters = state.contentTypeFilters.filter(f => f.selected)
    return selectedFilters.length > 0
  }

  const FilterContainerMobile = styled(FilterContainer)`
    flex-direction: row;
    margin: 28px 0 32px;
  `

  const MoreFiltersButton = styled.div<{ accentColor: string, open: boolean }>`
    color: ${p => p.accentColor};
    font-weight: 700;
    display: flex;
    align-items: center;
    svg:nth-child(1) {
      padding-right: 8px;
    }
    svg:nth-child(2) {
      padding-left: 8px;
    }
  `

  const Divider = styled.hr`
    border: 0;
    border-top: 2px solid rgba(0, 0, 0, .8);
    margin: 0 0 28px;
  `

  return (
    <OnlyMobile>
      <MoreFiltersButton ref={props.allFiltersButtonFocus} tabIndex={0} role='button' accentColor={state.accentColor} open={state.allFiltersOpen} onClick={openAllFilters} onKeyPress={e => onKeyEnter(e, openAllFilters)}>
        <SlidersIcon />
        {hasSelectedFilters() ? 'Lisää suodattimia' : 'Suodata tuloksia'}
        <ChevronDownIcon />
      </MoreFiltersButton>
      <FilterContainerMobile>
        {state.contentTypeFilters.filter(option => option.selected === true).map(option => (
          <FilterElement tabIndex={0} key={'content-type-' + option.id} accentColor={state.accentColor}
            onClick={() => toggleFilter('contentType', option.id)} selected={option.selected}
            role='checkbox' onKeyPress={e => onKeyEnter(e, () => toggleFilter('contentType', option.id))} aria-checked={option.selected}>
            {option.label}
            <ThinCloseIcon stroke={state.accentColor} style={{ paddingLeft: '8px' }} />
          </FilterElement>
        ))}
      </FilterContainerMobile>
      <Divider />
    </OnlyMobile>
  )
}
