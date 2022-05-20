import styled from 'styled-components'
import { useAppState } from '../../AppState'

const CheckboxIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="24" height="24" rx="2" fill="currentColor" />
    <path fillRule="evenodd" clipRule="evenodd" d="M9.74859 13.471C8.96813 12.7499 7.70639 11.4288 6.86579 10.5882C6.02517 9.80775 5.48455 10.4679 4.46339 11.5491C3.32199 12.6905 4.46339 13.2905 6.08527 14.9123L9.02827 17.8553C10.1095 18.8163 11.0103 17.3749 12.4517 15.9936L18.3377 10.0476C20.1994 8.24607 20.6197 8.24607 19.1181 6.80463C17.797 5.42339 17.8572 5.42339 15.7549 7.58509C14.794 8.48587 10.0495 13.2905 9.74873 13.4711L9.74859 13.471Z" fill="white"/>
  </svg>
)

const CheckedBox = styled.div<{ accentColor: string }>`
  opacity: 0;
  line-height: 24px;
  position: absolute;
  top: 0px;
  left: 0px;
  height: 24px;
  width: 24px;
  color: ${p => p.accentColor};
  svg {
    position: absolute;
    left: 0px;
    top: 0px;
    width: 24px;
    height: 24px;
  }
`

const UncheckedBox = styled.div`
  position: absolute;
  top: 0px;
  left: 0px;
  height: 24px;
  width: 24px;
  border: 1px solid rgba(0, 0, 0, .7);
  background-color: #fff;
  border-radius: 2px;
  box-sizing: border-box;
`

const PromotedCheckbox = styled.div`
  position: relative;
  width: 24px;
  height: 24px;
  margin-right: 8px;
  cursor: pointer;
  &:focus {
    outline: 2px solid #99f;
  }

  input:checked ~ ${UncheckedBox} {
    opacity: 0;
  }
  input:checked ~ ${CheckedBox} {
    opacity: 1;
  }
`

const HiddenRealInputCheckbox = styled.input`
  border: 0; 
  clip: rect(0 0 0 0); 
  height: 1px;
  width: 1px;
  margin: -1px; 
  overflow: hidden; 
  padding: 0; 
  position: absolute; 
`

interface CustomCheckboxProps {
  id: string
  label: string
  checked: boolean
  onChange?: () => void
  tabStopIndex: number
}
export const CustomCheckbox = (props: CustomCheckboxProps) => {
  const state = useAppState()
  const id = props.id

  const clickBox = (e: any) => {
    document.getElementById(id)?.click()
    e.preventDefault()
  }

  return (
    <PromotedCheckbox role='checkbox' aria-checked={props.checked} aria-label={props.label} tabIndex={props.tabStopIndex} onKeyPress={clickBox}>
      <HiddenRealInputCheckbox id={id} type='checkbox' checked={props.checked} onChange={props.onChange} tabIndex={-1} aria-hidden />
      <UncheckedBox />
      <CheckedBox accentColor={state.accentColor} onClick={clickBox}>
        <CheckboxIcon />
      </CheckedBox>   
    </PromotedCheckbox>
  )
}