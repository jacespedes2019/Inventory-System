import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect } from "react";
import { useProducts } from "../store/products";

const schema = z.object({
  name: z.string().min(1),
  description: z.string().optional(),
  price: z.coerce.number().min(0),
  quantity: z.coerce.number().int().min(0),
  image_url: z.string().url().optional().or(z.literal("")),
});

type FormValues = z.infer<typeof schema>;

export default function ProductFormModal({
  open, onClose, editId
}: {
  open: boolean;
  onClose: () => void;
  editId: number | null;
}) {
  const { items, create, update } = useProducts();
  const editing = editId ? items.find(i => i.id === editId) : undefined;

  const { register, handleSubmit, reset, formState: { errors, isSubmitting }, watch } =
    useForm<FormValues>({ resolver: zodResolver(schema) });

  useEffect(() => {
    if (editing) {
      reset({
        name: editing.name,
        description: editing.description ?? "",
        price: editing.price,
        quantity: editing.quantity,
        image_url: editing.image_url ?? "",
      });
    } else {
      reset({ name: "", description: "", price: 0, quantity: 0, image_url: "" });
    }
  }, [editing, reset]);

  const onSubmit = async (values: FormValues) => {
    const payload = {
      ...values,
      image_url: values.image_url ? values.image_url : null,
    };
    if (editId) await update(editId, payload);
    else await create(payload);
    onClose();
  };

  const preview = watch("image_url");

  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/40 grid place-items-center z-50">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">{editId ? "Edit product" : "New product"}</h3>
          <button className="text-gray-500" onClick={onClose}>✕</button>
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
              <input className="mt-1 w-full border rounded-lg px-3 py-2" type="number" step="0.01" {...register("price")} />
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
              <img src={preview} onError={(e)=>{(e.currentTarget as HTMLImageElement).style.display='none';}}
                   className="mt-2 w-24 h-24 object-cover rounded-lg" />
            ) : null}
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <button type="button" className="rounded-lg border px-4 py-2" onClick={onClose}>Cancel</button>
            <button className="rounded-lg bg-black text-white px-4 py-2" disabled={isSubmitting}>
              {editId ? "Save changes" : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}