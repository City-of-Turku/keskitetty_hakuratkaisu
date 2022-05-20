import { MouseEvent } from 'react'
import styled from 'styled-components'
import { useActions, useAppState } from '../../AppState'
import { ChevronDownIcon } from '../../assets/Icons'
import { Breakpoint } from '../../Constants'
import { Filter, FilterOption } from '../../Interfaces'
import { onKeyEnter } from '../../Utils'
import { CustomCheckbox } from '../atoms/CustomCheckbox'

const popupZIndex = 20

export const FilterElement = styled.div<{open?: boolean, selected?: boolean, accentColor: string}>`
  position: relative;
  cursor: pointer;
  font-weight: 400;
  padding: 10px 14px;
  border: 1px solid ${p => (p.open || p.selected ? p.accentColor : 'black')};
  background-color: ${p => p.selected ? p.accentColor : 'transparent'};
  color: ${p => p.selected ? 'white' : 'black'};
  border-radius: 20px;
  transition: .5s;
  display: flex;
  align-items: center;
  &:hover {
    border-style: solid;
  }
  &:focus {
    border-style: solid;
  }

  svg.chevronDownIcon {
    position: relative;
    top: -1px;
    margin-left: 8px;
    transition: .3s;
    transform: ${p => (p.open ? 'rotate(-180deg)' : 'none')};
  }
  svg.closeFilterIcon {
    color: #C82A07;
    position: relative;
    top: -1px;
    margin-left: 8px;
    transition: .4s;
  }
  svg.slidersIcon {
    margin-left: 8px;
  }
  &:hover {
    svg.closeFilterIcon {
      transform: rotate(90deg);
    }
  }
`

const FilterPopup = styled.div<{open: boolean}>`
  cursor: default;
  display: ${p => (p.open ? 'flex' : 'none')};
  position: absolute;
  top: 48px;
  left: 0px;
  padding: 8px;
  background-color: #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, .25);
  white-space: nowrap;
  flex-direction: column;
  gap: 4px;
  z-index: ${popupZIndex};

  @media (max-width: ${Breakpoint.Small}) {
    position: fixed;
    top: initial;
    bottom: 0;
    left: 0;
    right: 0;
  }
`

const PopupOverlay = styled.div<{open?: boolean}>`
  display: ${p => (p.open ? 'block' : 'none')};
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: ${popupZIndex - 1};
`

const FilterRow = styled.label`
  display: grid;
  align-items: center;
  grid-template-columns: auto auto 1fr;
  padding: 14px 20px;
  cursor: pointer;
  &:hover {
    color: #000;
    background-color: rgba(0, 0, 0, .1);
    border-radius: 4px;
  }
  span {
    padding-left: 4px;
    font-weight: 400;
  }
  .number {
    padding-left: 106px;
    text-align: right;
  }
`

interface FilterGroupProps {
  filter: Filter
  options: FilterOption[]
}
export const FilterGroup = (p: FilterGroupProps) => {
  const state = useAppState()
  const actions = useActions()

  const filter = p.filter
  const options = p.options

  // when clicking the FilterPopup, do not propagate clicks to the parent FilterElement
  const noPropagate = (e: MouseEvent<HTMLDivElement>) => {
    e.stopPropagation()
  }

  const onChange = (optionId: string) => {
    // TODO refactor. duplicate code, see also AllFiltersOverlay.tsx
    const newOptions: FilterOption[] = []
    for (const option of options) {
      const newOption = {...option}
      if (newOption.id === optionId) {
        newOption.selected = !newOption.selected
      }
      newOptions.push(newOption)
    }
    actions.setContentTypeFilters(newOptions)
    actions.setRefreshSearch()
  }

  const isOptionsSelected = () => {
    for (const option of options) {
      if (option.selected) return true
    }
    return false
  }

  const isOptionSelected = (optionId: string) => {
    for (const option of options) {
      if (option.id === optionId && option.selected) return true
    }
    return false
  }

  const open = state.contentTypeFiltersOpen
  return (
    <>
      <FilterElement tabIndex={0} accentColor={state.accentColor} open={open} selected={isOptionsSelected()}
        onClick={() => actions.setContentTypeFiltersOpen(!state.contentTypeFiltersOpen)}
        onKeyPress={e => onKeyEnter(e, () => actions.setContentTypeFiltersOpen(!state.contentTypeFiltersOpen))}>
        {filter.label} <ChevronDownIcon />

        <FilterPopup open={open} onClick={noPropagate}>
          {options.map(option => (
            <FilterRow key={filter.id + option.id} htmlFor={filter.id + option.id}>
              <CustomCheckbox id={filter.id + option.id} label={option.label} checked={isOptionSelected(option.id)} onChange={() => onChange(option.id)} tabStopIndex={0} />
              <span>{option.label}</span>
              <div className='number'>{/* TODO number of hits in this group */}</div>
            </FilterRow>
          ))}
        </FilterPopup>
      </FilterElement>
      <PopupOverlay open={open} onClick={() => actions.setContentTypeFiltersOpen(false)} />
    </>
  )
}