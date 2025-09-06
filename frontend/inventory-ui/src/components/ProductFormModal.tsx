/**
 * File: ProductFormModal.tsx
 * Description: Modal form to create or edit a product.
 * Author: Jairo Céspedes
 * Date: 2025-09-05
 *
 * Responsibilities:
 * - Render controlled form for product fields (name, price, qty, image).
 * - Validate inputs using react-hook-form + zod.
 * - Submit create or update requests to product store.
 *
 * Notes:
 * - Closes modal automatically on success.
 * - Shows preview of product image when URL is entered.
 */
import { useEffect } from "react";
import { useForm, type SubmitHandler } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useProducts } from "../store/products";

const schema = z.object({
  name: z.string().min(1, "Name is required"),
  description: z.string().optional(),
  // Use z.coerce to accept string inputs and coerce to number
  price: z.coerce.number().min(0, "Price must be >= 0"),
  quantity: z.coerce.number().int("Quantity must be an integer").min(0, "Quantity must be >= 0"),
  // Allow empty string or valid URL
  image_url: z.union([z.literal(""), z.string().url("Invalid URL")]).optional(),
});

type FormValues = z.infer<typeof schema>;

const EMPTY: FormValues = { name: "", description: "", price: 0, quantity: 0, image_url: "" };

export default function ProductFormModal({
  open,
  onClose,
  editId,
}: {
  open: boolean;
  onClose: () => void;
  editId: number | null;
}) {
  const { items, create, update } = useProducts();
  const editing = editId ? items.find((i) => i.id === editId) : undefined;

  const {
  register,
  handleSubmit,
  reset,
  formState: { errors, isSubmitting },
  watch,
} = useForm<FormValues>({
  resolver: zodResolver(schema) as any,
  defaultValues: EMPTY,
  shouldUnregister: true,
});

  useEffect(() => {
  if (!open) return; // solo actuamos al abrir
  if (editing) {
    reset({
      name: editing.name,
      description: editing.description ?? "",
      price: Number(editing.price ?? 0),
      quantity: Number(editing.quantity ?? 0),
      image_url: editing.image_url ?? "",
    });
  } else {
    reset(EMPTY);
  }
}, [open, editId, editing, reset]);

  // 👉 Tipamos también el SubmitHandler
  const onSubmit: SubmitHandler<FormValues> = async (values) => {
    const payload = {
      ...values,
      image_url: values.image_url ? values.image_url : null,
    };
    if (editId) {
      await update(editId, payload);
    } else {
      await create(payload);
    }
    onClose();
  };

  const preview = watch("image_url");

  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/40 grid place-items-center z-50">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">{editId ? "Edit product" : "New product"}</h3>
          <button className="text-gray-500" onClick={onClose}>
            ✕
          </button>
        </div>

        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
          <div>
            <label className="block text-sm font-medium">Name</label>
            <input className="mt-1 w-full border rounded-lg px-3 py-2" {...register("name")} />
            {errors.name && <p className="text-sm text-red-600">{errors.name.message}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium">Description</label>
            <textarea className="mt-1 w-full border rounded-lg px-3 py-2" rows={3} {...register("description")} />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium">Price</label>
              <input
                className="mt-1 w-full border rounded-lg px-3 py-2"
                type="number"
                step="0.01"
                {...register("price")}
              />
              {errors.price && <p className="text-sm text-red-600">{errors.price.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium">Quantity</label>
              <input className="mt-1 w-full border rounded-lg px-3 py-2" type="number" {...register("quantity")} />
              {errors.quantity && <p className="text-sm text-red-600">{errors.quantity.message}</p>}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium">Image URL</label>
            <input className="mt-1 w-full border rounded-lg px-3 py-2" placeholder="https://..." {...register("image_url")} />
            {preview ? (
              <img
                src={preview}
                onError={(e) => {
                  (e.currentTarget as HTMLImageElement).style.display = "none";
                }}
                className="mt-2 w-24 h-24 object-cover rounded-lg"
              />
            ) : null}
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <button type="button" className="rounded-lg border px-4 py-2" onClick={onClose}>
              Cancel
            </button>
            <button className="rounded-lg bg-black text-white px-4 py-2" disabled={isSubmitting}>
              {editId ? "Save changes" : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}