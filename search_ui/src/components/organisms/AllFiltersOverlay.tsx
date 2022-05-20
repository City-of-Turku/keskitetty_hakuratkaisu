import { RefObject, useState, KeyboardEvent } from 'react'
import styled from 'styled-components'
import { useActions, useAppState } from '../../AppState'
import { CloseIcon, MinusIcon, PlusIcon, SlidersIcon } from '../../assets/Icons'
import { contentTypeFilter, FilterOption } from '../../Interfaces'
import { onKeyEnter } from '../../Utils'
import { WhiteButton, RedButton } from '../atoms/Buttons'
import { CustomCheckbox } from '../atoms/CustomCheckbox'

const AllFiltersOverlayContainer = styled.div<{ visible: boolean }>`
  position: fixed;
  top: 0;
  right: ${p => p.visible ? '0px' : '-576px'};
  padding: 32px;
  width: 512px;
  max-width: 100%;
  box-sizing: border-box;
  background-color: #fff;
  height: 100%;
  transition: 1s;
  z-index: 9;

  display: flex;
  flex-direction: column;
  justify-content: space-between;
`

const TopHeading = styled.h2`
  font-size: 1.5em;
  font-weight: 700;
  margin: 0;
`
const TopContainer = styled.div`
  display: flex;
  align-items: center;
  padding-bottom: 32px;
  /* border-bottom: 2px solid #000; */

  svg.slidersIcon {
    width: 32px;
    height: 32px;
    margin-right: 12px;
  }
  ${TopHeading} {
    flex-grow: 1;
  }
  svg.closeIcon {
    cursor: pointer;
  }
`

const TopSeparator = styled.div`
  height: 0;
  border-bottom: 2px solid rgba(0, 0, 0, .8);
  margin: 0 -16px;
`

const FilterContainer = styled.div<{ accentColor: string }>`
  padding: 28px 0;
  border-bottom: 1px solid rgba(0, 0, 0, .3);
  svg {
    color: ${p => p.accentColor};
  }
`

const SpaceBetween = styled.div<{ marginBottom?: number }>`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${p => p.marginBottom ? p.marginBottom : 0}px;
  svg.plusIcon, svg.minusIcon {
    cursor: pointer;
  }
`

const FilterHeading = styled.div`
  font-weight: 700;
`

const Labels = styled.div`
  margin-top: 4px;
  color: rgba(0, 0, 0, .5);
  display: flex;
  flex-wrap: wrap;
`
const Label = styled.div`
  display: inline;
  margin-right: 8px;
`

const Options = styled.div`
`

const FilterSelection = styled.div`
  display: flex;
  align-items: center;
  padding: 14px 0;
`

interface AllFiltersOverlayProps {
  visible: boolean
  close: () => void
  allFiltersPanelFocus: RefObject<HTMLDivElement>
  allFiltersButtonFocus: RefObject<HTMLDivElement>
}
export const AllFiltersOverlay = (props: AllFiltersOverlayProps) => {
  const state = useAppState()
  const actions = useActions()
  const [openFilterIds, setOpenFilterIds] = useState<string[]>([contentTypeFilter.id]) // content type group is open by default
  const tabStopIndex = props.visible ? 0 : -1 // stop focus on given element, but only when this modal is open

  const removeOpenFilterId = (id: string) => {
    const filtered = openFilterIds.filter(s => s !== id)
    setOpenFilterIds(filtered)
  }

  const addOpenFilterId = (id: string) => {
    const added = [...openFilterIds]
    added.push(id)
    setOpenFilterIds(added)
  }

  const FilterTypeHeading = ({id, heading, closed}: {id: string, heading: string, closed: boolean}) => {
    const onClick = () => {
      closed ? addOpenFilterId(id) : removeOpenFilterId(id)
    }
    const label = () => {
      return 'Suodatin: ' + heading + ', ' + (closed ? 'avaa vaihtoehdot' : 'sulje vaihtoehdot')
    }
    return (
      <SpaceBetween marginBottom={closed ? 4 : 16}>
        <FilterHeading>{heading}</FilterHeading>
        <div tabIndex={tabStopIndex} onClick={onClick} role='button' onKeyPress={e => onKeyEnter(e, onClick)} aria-label={label()} aria-expanded={!closed}>
          {closed ? <PlusIcon /> : <MinusIcon />}
        </div>
      </SpaceBetween>
    )
  }

  interface FilterDataItem {
    id: string
    label: string
    options: FilterOption[]
  }
  const filterData: FilterDataItem[] = [
    {
      id: contentTypeFilter.id,
      label: contentTypeFilter.label,
      options: state.contentTypeFilters,
    },
    // TODO add more filters when we support those
  ]

  const filterOptionClicked = (filterId: string, optionId: string) => {
    console.log('filterOptionClicked', { filterId, optionId })
    if (filterId === contentTypeFilter.id) {
      const options = state.contentTypeFilters
      // TODO refactor, this is duplicated code, see also FilterGroup.tsx
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
  }

  const clearAll = () => {
    const options = state.contentTypeFilters
    const newOptions: FilterOption[] = []
    for (const option of options) {
      const newOption = {...option}
      newOption.selected = false
      newOptions.push(newOption)
    }
    actions.setContentTypeFilters(newOptions)
    actions.setRefreshSearch()
}

  const closePanel = () => {
    props.close()
    if (props.allFiltersButtonFocus?.current) {
      props.allFiltersButtonFocus.current.focus()
    }
  }

  const onKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.code === 'Escape') {
      closePanel()
    }
  }

  return (
    <AllFiltersOverlayContainer visible={props.visible} aria-hidden={!props.visible} aria-live='polite' role='group' aria-label='Kaikki suodattimet' tabIndex={tabStopIndex} ref={props.allFiltersPanelFocus} onKeyDown={onKeyDown}>
      <div>
        <TopContainer>
          <SlidersIcon />
          <TopHeading>Kaikki suodattimet</TopHeading>
          <div tabIndex={tabStopIndex} role='button' aria-label='Sulje kaikki suodattimet' onClick={closePanel} onKeyPress={e => onKeyEnter(e, closePanel)}>
            <CloseIcon />
          </div>
        </TopContainer>
        <TopSeparator />

        {filterData.map(fd => {
          const closed = openFilterIds.indexOf(fd.id) === -1
          return (
            <FilterContainer key={fd.id} accentColor={state.accentColor}>
              <FilterTypeHeading id={fd.id} heading={fd.label} closed={closed} />
              {closed ?
                <Labels>
                  {fd.options
                    .filter(option => option.selected === true)
                    .map(option => <Label>{option.label}</Label>)}
                </Labels>
              : <Options>
                {fd.options.map(option => (
                  <FilterSelection key={option.id}>
                    <CustomCheckbox id={'afp:' + fd.id + option.id} label={option.label} checked={option.selected} onChange={() => filterOptionClicked(fd.id, option.id)} tabStopIndex={tabStopIndex} />
                    <label htmlFor={'afp:' + fd.id + option.id} id={'afp:' + fd.id + option.id}>{option.label}</label>
                  </FilterSelection>
                ))}
                </Options>
              }
            </FilterContainer>
          )
        })}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
        <WhiteButton tabIndex={tabStopIndex} accentColor='#fff' onClick={clearAll}>Tyhjennä kaikki</WhiteButton>
        <RedButton tabIndex={tabStopIndex} accentColor={state.accentColor} onClick={closePanel} onKeyPress={e => onKeyEnter(e, closePanel)}>Näytä</RedButton>
      </div>

    </AllFiltersOverlayContainer>
  )
}