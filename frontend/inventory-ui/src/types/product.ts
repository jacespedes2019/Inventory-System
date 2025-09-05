export type ProductOut = {
  id: number;
  name: string;
  description?: string | null;
  price: number;
  quantity: number;
  image_url?: string | null;
  updated_at: string; // ISO
};

export type ProductCreate = {
  name: string;
  description?: string | null;
  price: number;
  quantity: number;
  image_url?: string | null;
};

export type ProductUpdate = Partial<ProductCreate>;