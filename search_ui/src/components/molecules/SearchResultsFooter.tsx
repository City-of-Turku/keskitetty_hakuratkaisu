import styled from 'styled-components'
import { useAppState } from '../../AppState'
import { PlusIcon, UpArrowIcon } from '../../assets/Icons'
import { onKeyEnter } from '../../Utils'
import { SeparatorLine } from "../atoms/SeparatorLine"

interface SearchResultsFooterProps {
  instanceId: string
  more: boolean
  onShowMore: () => void
}
export const SearchResultsFooter = (props: SearchResultsFooterProps) => {
  const state = useAppState()
  
  const toTop = () => {
    // scroll window to top
    const e = document.querySelector('#keha-instance-' + props.instanceId + ' .back-to-top')
    if (e) {
      e.scrollIntoView({ behavior: 'smooth' })
    } else {
      window.scrollTo({ top: 0, left: 0, behavior: 'smooth' })
    }

    // keyboard focus on search input field element
    const sf = document.querySelector('#keha-search-field-' + props.instanceId) as HTMLInputElement
    sf?.focus()
  }

  return (
    <div>
      <SeparatorLine />
      <Container>
        <VerticallyCentered tabIndex={0} accentColor={state.accentColor} onClick={props.onShowMore} onKeyPress={e => onKeyEnter(e, props.onShowMore)} role='button'>
          {props.more ?
            <>
              <PlusIcon />
              <FooterLink accentColor={state.accentColor}>
                <strong>Näytä lisää</strong> hakutuloksia…
              </FooterLink>
            </> :
            <div />
          }
        </VerticallyCentered>
        <VerticallyCentered tabIndex={0} accentColor={state.accentColor} onClick={toTop} onKeyPress={e => onKeyEnter(e, toTop)} role='button'>
          <FooterLink accentColor={state.accentColor}>
            <strong>Takaisin ylös</strong>
          </FooterLink>
          <UpArrowIcon />
        </VerticallyCentered>
      </Container>
    </div>
  )
}

const VerticallyCentered = styled.div<{ accentColor: string }>`
  display: flex;
  align-items: center;
  cursor: pointer;
  svg {
    color: ${p => p.accentColor};
  }
`

const Container = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 32px;

  ${VerticallyCentered}:first-child {
    svg {
      margin-right: 6px;
    }
  }
  ${VerticallyCentered}:last-child {
    svg {
      margin-left: 6px;
    }
  }
`

const FooterLink = styled.div<{ accentColor: string }>`
  transition: .4s;
  &:hover {
    color: ${p => p.accentColor};
    text-decoration: underline;
  }
`