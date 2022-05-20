import { useState } from 'react'
import styled from 'styled-components'
import { LookingGlassIcon } from '../assets/Icons'
import { SearchPage } from './SearchPage'

const WidgetContainer = styled.div`
  position: relative;
  display: grid;
  align-items: center;
`

const InputField = styled.div`
  border: 0;
  height: 16px;
  font-size: 1em;
  padding: 8px 8px;
  color: #000;
  border-bottom: 1px solid #000;
  padding-left: 32px;
  background-color: transparent;
  cursor: pointer;
`

const Icon = styled.div<{ accentColor: string}>`
  position: absolute;
  top: 4px;
  left: 4px;
  color: ${p => p.accentColor};
  cursor: pointer;
  width: 16px;
  height: 16px;
  font-size: 1em;
  &:hover {
    color: black;
  }
`

const SearchResultsModal = styled.div<{ visible: boolean }>`
  position: fixed;
  z-index: 9;
  transition: .5s;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  overflow: scroll;
  background-color: #fff;
  opacity: ${p => p.visible ? 1 : 0};
  visibility: ${p => p.visible ? 'visible' : 'hidden'};
  color: #000;

  p {
    margin: 0 0 1.5em 0;
  }
`

const ModalContainer = styled.div`
  position: relative;
  padding: 48px 16px 0;
`

export const SearchWidget = (props: { instanceId: string }) => {
  const [modalOpen, setModalOpen] = useState(false)
  
  const openModal = () => {
    inlineApplicationDisplay(false)
    setModalOpen(true)
    setTimeout(() => document.getElementById(`keha-search-field-${props.instanceId}`)?.focus(), 100)
  }

  const closeModal = () => {
    inlineApplicationDisplay(true)
    setModalOpen(false)
  }

  const inlineApplicationDisplay = (b: boolean) => {
    // if a web page contains both versions of the search ui (inline and widget),
    // then some popups (e.g. content type filter popup) would open in both versions.
    // => here we will completely hide the underlying inline version, so that the popup
    // is also hidden. 
    var inline = document.querySelector('.keha-ui-application-inline') as any
    if (inline && inline.style) {
      inline.style.display = b ? 'block' : 'none'
    }
  }

  return (
    <>
      <WidgetContainer onClick={openModal}>
        <Icon accentColor='#000'><LookingGlassIcon /></Icon>
        <InputField role='button' aria-label='Avaa haku' tabIndex={0} />
      </WidgetContainer>

      <SearchResultsModal visible={modalOpen}>
        <div className='back-to-top'></div>
        <ModalContainer>
          <SearchPage instanceId={props.instanceId} widget onClose={closeModal} />
        </ModalContainer>
      </SearchResultsModal>
    </>
  )
}