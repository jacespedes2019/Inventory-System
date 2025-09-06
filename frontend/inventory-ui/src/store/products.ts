/**
 * File: products.ts
 * Description: Zustand store for managing products and their CRUD operations.
 * Author: Jairo Céspedes
 * Date: 2025-09-05
 *
 * Responsibilities:
 * - Manage product list and state (loading, error).
 * - Provide methods for listing, creating, updating, and deleting products.
 * - Support search, filtering, and sorting queries.
 *
 * Notes:
 * - Uses the preconfigured Axios client.
 * - State is reactive and consumed in Dashboard and components.
 */

import { create } from "zustand";
import { ProductsRepo } from "../repositories/products.repo";
import type { ProductCreate, ProductOut, ProductUpdate } from "../types/product";

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
    // Defensive: clear previous errors and set loading
    set({ loading: true, error: null });
    try {
      const data = await ProductsRepo.list(query);
      set({ items: data, loading: false });
    } catch (e: any) {
      // Map error to user-friendly message
      set({ error: e?.message ?? "Failed to fetch products", loading: false });
    }
  },

  async create(payload) {
    try {
      const data = await ProductsRepo.create(payload);
      set({ items: [data, ...get().items] });
      return data;
    } catch (e: any) {
      set({ error: e?.message ?? "Failed to create product" });
      throw e;
    }
  },

  async update(id, payload) {
    try {
      const data = await ProductsRepo.update(id, payload);
      set({ items: get().items.map((it) => (it.id === id ? data : it)) });
      return data;
    } catch (e: any) {
      set({ error: e?.message ?? "Failed to update product" });
      throw e;
    }
  },

  async remove(id) {
    // Optional: optimistic update + rollback on failure
    const prev = get().items;
    set({ items: prev.filter((it) => it.id !== id) });
    try {
      await ProductsRepo.remove(id);
    } catch (e: any) {
      set({ items: prev, error: e?.message ?? "Failed to delete product" });
      throw e;
    }
  },
}));