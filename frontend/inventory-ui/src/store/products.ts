import { create } from "zustand";
import type { ProductCreate, ProductOut, ProductUpdate } from "../types/product";
import client from "../api/client";

export type ListQuery = {
  q?: string;
  min_price?: number;
  max_price?: number;
  min_qty?: number;
  has_image?: boolean;
  sort_by?: "name" | "price" | "quantity" | "updated_at";
  sort_dir?: "asc" | "desc";
};

type ProductsState = {
  items: ProductOut[];
  loading: boolean;
  error: string | null;
  list: (query?: ListQuery) => Promise<void>;
  create: (payload: ProductCreate) => Promise<ProductOut>;
  update: (id: number, payload: ProductUpdate) => Promise<ProductOut>;
  remove: (id: number) => Promise<void>;
};

export const useProducts = create<ProductsState>((set, get) => ({
  items: [],
  loading: false,
  error: null,

  async list(query) {
    set({ loading: true, error: null });
    const params: Record<string, any> = {};
    if (query) {
      for (const [k, v] of Object.entries(query)) {
        if (v !== undefined && v !== null && v !== "") params[k] = v;
      }
    }
    const { data } = await client.get<ProductOut[]>("/products/", { params });
    set({ items: data, loading: false });
  },

  async create(payload) {
    const { data } = await client.post<ProductOut>("/products/", payload);
    set({ items: [data, ...get().items] });
    return data;
  },

  async update(id, payload) {
    const { data } = await client.put<ProductOut>(`/products/${id}`, payload);
    set({ items: get().items.map((it) => (it.id === id ? data : it)) });
    return data;
  },

  async remove(id) {
    await client.delete(`/products/${id}`);
    set({ items: get().items.filter((it) => it.id !== id) });
  },
}));