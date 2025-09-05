/**
 * File: ProductTable.tsx
 * Description: Table component to list products with actions.
 * Author: Jairo Céspedes
 * Date: 2025-09-05
 *
 * Responsibilities:
 * - Render product list with name, price, quantity, and updated date.
 * - Provide buttons for view, edit, and delete actions.
 *
 * Notes:
 * - Requires parent props for onEdit, onView, and admin permissions.
 */
import { useProducts } from "../store/products";
import type { ProductOut } from "../types/product";


export default function ProductTable({
  items, loading, isAdmin, onEdit, onView,
}: {
  items: ProductOut[];
  loading: boolean;
  isAdmin: boolean;
  onEdit: (id: number) => void;
  onView: (id: number) => void;
}) {
  const { remove } = useProducts();

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full">
        <thead className="bg-gray-100 text-left">
          <tr>
            <th className="p-3">Image</th>
            <th className="p-3">Name</th>
            <th className="p-3">Price</th>
            <th className="p-3">Qty</th>
            <th className="p-3">Updated</th>
            <th className="p-3"></th>
          </tr>
        </thead>
        <tbody>
          {loading && <tr><td className="p-4" colSpan={6}>Loading...</td></tr>}
          {!loading && items.length === 0 && (
            <tr><td className="p-4 text-gray-500" colSpan={6}>No products found</td></tr>
          )}
          {!loading && items.map((p) => (
            <tr key={p.id} className="border-t">
              <td className="p-3">
                {p.image_url ? (
                  <img src={p.image_url} alt={p.name} className="w-12 h-12 object-cover rounded-lg" />
                ) : (
                  <div className="w-12 h-12 bg-gray-200 rounded-lg grid place-items-center text-xs text-gray-500">no img</div>
                )}
              </td>
              <td className="p-3">{p.name}</td>
              <td className="p-3">${Number(p.price ?? 0).toFixed(2)}</td>
              <td className="p-3">{p.quantity}</td>
              <td className="p-3">{new Date(p.updated_at).toLocaleString()}</td>
              <td className="p-3">
                <div className="flex gap-3">
                  <button className="text-gray-700 hover:underline" onClick={() => onView(p.id)}>View</button>
                  {isAdmin && (
                    <>
                      <button className="text-blue-600 hover:underline" onClick={() => onEdit(p.id)}>Edit</button>
                      <button className="text-red-600 hover:underline" onClick={() => remove(p.id)}>Delete</button>
                    </>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}