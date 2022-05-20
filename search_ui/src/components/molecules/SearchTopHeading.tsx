import styled from 'styled-components'
import { NudeButton } from '../atoms/Buttons'
import { CloseIcon }  from '../../assets/Icons'
import { Breakpoint } from '../../Constants'

interface SearchTopHeadingProps {
  widget?: boolean
  onClose?: () => void
}
export const SearchTopHeading = (props: SearchTopHeadingProps) => {
  if (!props.widget) return null
  return (
    <TopContainer>
      <TopTitle>Hae etsimäsi</TopTitle>
      <CloseSearch onClick={props.onClose}>
        <NudeButton onClick={props.onClose}>Sulje haku</NudeButton>
        <CloseIcon />
      </CloseSearch>
    </TopContainer>
  )
}

const TopContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 0 32px;
`

const TopTitle = styled.h2`
  font-size: 2.5em;
  font-weight: 700;
  margin: 0;
  @media (max-width: ${Breakpoint.Small}) {
    font-size: 1.5em;
  }
`

const CloseSearch = styled.div`
  padding: 12px 0 12px 12px;
  display: flex;
  align-items: center;
  font-weight: 700;
  cursor: pointer;
  button {
    margin-right: 12px;
  }
`
