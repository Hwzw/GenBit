import { create } from "zustand";
import type { ConstructElement, OrganismSearchResult } from "@/types";

interface DesignerState {
  elements: ConstructElement[];
  selectedOrganism: OrganismSearchResult | null;

  addElement: (element: ConstructElement) => void;
  removeElement: (index: number) => void;
  updateElement: (index: number, element: ConstructElement) => void;
  reorderElements: (fromIndex: number, toIndex: number) => void;
  clearElements: () => void;
  setSelectedOrganism: (organism: OrganismSearchResult | null) => void;
}

export const useDesignerStore = create<DesignerState>((set) => ({
  elements: [],
  selectedOrganism: null,

  addElement: (element) =>
    set((state) => ({
      elements: [
        ...state.elements,
        { ...element, position: state.elements.length },
      ],
    })),

  removeElement: (index) =>
    set((state) => ({
      elements: state.elements
        .filter((_, i) => i !== index)
        .map((el, i) => ({ ...el, position: i })),
    })),

  updateElement: (index, element) =>
    set((state) => ({
      elements: state.elements.map((el, i) => (i === index ? element : el)),
    })),

  reorderElements: (fromIndex, toIndex) =>
    set((state) => {
      const newElements = [...state.elements];
      const [moved] = newElements.splice(fromIndex, 1);
      newElements.splice(toIndex, 0, moved);
      return {
        elements: newElements.map((el, i) => ({ ...el, position: i })),
      };
    }),

  clearElements: () => set({ elements: [] }),

  setSelectedOrganism: (organism) => set({ selectedOrganism: organism }),
}));
