/**
 * File: DashboardPage.tsx
 * Description: Main dashboard for product management.
 * Author: Jairo Céspedes
 * Date: 2025-09-05
 *
 * Responsibilities:
 * - Display filters for searching, sorting, and filtering products.
 * - Render inventory table with products.
 * - Handle product creation, editing, and viewing via modals.
 *
 * Notes:
 * - Access is role-based (admin can edit/delete, user is read-only).
 * - Uses Zustand stores for reactive state.
 */
import { useEffect, useState } from "react";
import { useAuth } from "../store/auth";
import { useProducts } from "../store/products";
import Topbar from "../components/Topbar";
import ProductTable from "../components/ProductTable";
import ProductFormModal from "../components/ProductFormModal";
import ProductDetailModal from "../components/ProductDetailModal";



export default function DashboardPage() {
  const email = useAuth((s) => s.email);
  const role = useAuth((s) => s.role);
  const isAdmin = role === "admin";

  const { items, list, loading } = useProducts();

  const [q, setQ] = useState("");
  const [minPrice, setMinPrice] = useState<string>("");
  const [maxPrice, setMaxPrice] = useState<string>("");
  const [minQty, setMinQty] = useState<string>("");
  const [hasImage, setHasImage] = useState<"" | "true" | "false">("");
  const [sortBy, setSortBy] = useState<"name" | "price" | "quantity" | "updated_at">("name");
  const [sortDir, setSortDir] = useState<"asc" | "desc">("asc");

  const [openForm, setOpenForm] = useState(false);
  const [editId, setEditId] = useState<number | null>(null);

  const [openDetail, setOpenDetail] = useState(false);
  const [detailId, setDetailId] = useState<number | null>(null);

  useEffect(() => {
    list({
      q: q || undefined,
      min_price: minPrice ? Number(minPrice) : undefined,
      max_price: maxPrice ? Number(maxPrice) : undefined,
      min_qty: minQty ? Number(minQty) : undefined,
      has_image: hasImage === "" ? undefined : hasImage === "true",
      sort_by: sortBy,
      sort_dir: sortDir,
    });
  }, [q, minPrice, maxPrice, minQty, hasImage, sortBy, sortDir, list]);

  const productForDetail = detailId ? items.find(i => i.id === detailId) ?? null : null;

  return (
    <div className="min-h-screen bg-gray-50">
      <Topbar email={email ?? ""} />
      <div className="max-w-6xl mx-auto p-4 space-y-4">
        {/* Filters */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-7 gap-3 bg-white p-4 rounded-xl shadow">
        {/* Each field gets w-full so it doesn't overflow its grid cell */}
        <input
            className="border rounded-lg px-3 py-2 w-full"
            placeholder="Search by name"
            value={q}
            onChange={e => setQ(e.target.value)}
        />
        <input
            className="border rounded-lg px-3 py-2 w-full"
            placeholder="Min price"
            value={minPrice}
            onChange={e => setMinPrice(e.target.value)}
        />
        <input
            className="border rounded-lg px-3 py-2 w-full"
            placeholder="Max price"
            value={maxPrice}
            onChange={e => setMaxPrice(e.target.value)}
        />
        <input
            className="border rounded-lg px-3 py-2 w-full"
            placeholder="Min qty"
            value={minQty}
            onChange={e => setMinQty(e.target.value)}
        />
        <select
            className="border rounded-lg px-3 py-2 w-full"
            value={hasImage}
            onChange={e => setHasImage(e.target.value as any)}
        >
            <option value="">Image?</option>
            <option value="true">Only with image</option>
            <option value="false">Only without image</option>
        </select>

        {/* Last group: give it more room and prevent overflow */}
        <div className="min-w-0 md:col-span-2 flex gap-2">
            <select
            className="border rounded-lg px-3 py-2 w-full"
            value={sortBy}
            onChange={e => setSortBy(e.target.value as any)}
            >
            <option value="name">Name</option>
            <option value="price">Price</option>
            <option value="quantity">Quantity</option>
            <option value="updated_at">Updated</option>
            </select>
            <select
            className="border rounded-lg px-3 py-2 w-28 md:w-32"
            // ^ fixed width so the pair doesn't push outside
            value={sortDir}
            onChange={e => setSortDir(e.target.value as any)}
            >
            <option value="asc">Asc</option>
            <option value="desc">Desc</option>
            </select>
        </div>
        </div>

        {/* Actions */}
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold">Inventory</h2>
          {isAdmin && (
            <button
              className="rounded-xl bg-black text-white px-4 py-2"
              onClick={() => { setEditId(null); setOpenForm(true); }}
            >
              New product
            </button>
          )}
        </div>

        {/* Table */}
        <div className="bg-white rounded-xl shadow overflow-hidden">
          <ProductTable
            items={items}
            loading={loading}
            isAdmin={isAdmin}
            onEdit={(id) => { setEditId(id); setOpenForm(true); }}
            onView={(id) => { setDetailId(id); setOpenDetail(true); }}
          />
        </div>
      </div>

      {/* Modals */}
      <ProductFormModal open={openForm} onClose={() => setOpenForm(false)} editId={editId} />
      <ProductDetailModal open={openDetail} onClose={() => setOpenDetail(false)} product={productForDetail} />
    </div>
  );
}