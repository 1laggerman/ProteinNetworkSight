import { GlobalState } from "little-state-machine";
import {
  INamesStringMap,
  IVectorsValues,
  threshMap,
} from "../@types/global";

import { ISuggestionsJson, OptionType } from "../@types/json";

export function updateIsLoading(
  state: GlobalState,
  payload: { isLoading: boolean }
): GlobalState {
  console.log(payload);
  return {
    ...state,
    ...payload,
  };
}
export function updateShowError(
  state: GlobalState,
  payload: { showError: boolean }
): GlobalState {
  console.log(payload);
  return {
    ...state,
    ...payload,
  };
}

export function updateFileName(
  state: GlobalState,
  payload: { fileName: string }
): GlobalState {
  console.log(payload);
  return {
    ...state,
    ...payload,
  };
}

export function updateFileUpload(
  state: GlobalState,
  payload: { json: any[]; headers: string[] }
): GlobalState {
  console.log(payload);
  return {
    ...state,
    ...payload,
  };
}

export function updateFileDetails(
  state: GlobalState,
  payload: {
    proteinsNames: string[];
    scoreThreshold: number;
    positiveThreshold: number;
    negativeThreshold: number;
    organism: OptionType;
    vectorsHeaders: string[];
    thresholds: {[x: string]: number[];}
    // vectorsValues: IVectorsValues;
  }
): GlobalState {
  console.log(payload);
  return {
    ...state,
    ...payload,
  };
}

export function updateSuggestionsObj(
  state: GlobalState,
  payload: { suggestionsObj: ISuggestionsJson }
): GlobalState {
  console.log(payload);
  return {
    ...state,
    ...payload,
    isSetSuggestions: true,
  };
}


export function updateNamesMap(
  state: GlobalState,
  payload: { namesStringMap: INamesStringMap }
): GlobalState {
  console.log(payload);
  return {
    ...state,
    ...payload,
    isSetNamesMap: true,

  };
}

export function updateUuid(
  state: GlobalState,
  payload: { uuid: string }
): GlobalState {
  console.log(payload);
  return {
    ...state,
    ...payload,
  };
}


export function updateThresholds(
  state: GlobalState,
  payload: { thresholds: { [x: string]: number[]; }}
): GlobalState {
  console.log(payload);
  return {
    ...state,
    ...payload,
  };
}