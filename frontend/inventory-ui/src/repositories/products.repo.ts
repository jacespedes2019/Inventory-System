// Purpose: Pure data access for products (no UI state here).
import client from "../api/client";
import type { ProductCreate, ProductOut, ProductUpdate } from "../types/product";
import type { ListQuery } from "../store/products";

export const ProductsRepo = {
  list: (query?: ListQuery) =>
    client.get<ProductOut[]>("/products/", { params: query }).then(r => r.data),

  create: (payload: ProductCreate) =>
    client.post<ProductOut>("/products/", payload).then(r => r.data),

  update: (id: number, payload: ProductUpdate) =>
    client.put<ProductOut>(`/products/${id}`, payload).then(r => r.data),

  remove: (id: number) =>
    client.delete<void>(`/products/${id}`).then(r => r.data),
};
