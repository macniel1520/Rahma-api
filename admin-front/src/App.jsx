import { createContext, useContext, useEffect, useState } from "react";
import {
  Navigate,
  NavLink,
  Route,
  Routes,
  useNavigate,
  useParams,
  useSearchParams,
} from "react-router-dom";

const ACCESS_TOKEN_KEY = "rahma_panel_access_token";
const REFRESH_TOKEN_KEY = "rahma_panel_refresh_token";
const BootstrapContext = createContext({
  resources: [],
  actions: { paths: {}, components: { schemas: {} } },
  sections: [],
});

function readTokens() {
  return {
    accessToken: window.localStorage.getItem(ACCESS_TOKEN_KEY) || "",
    refreshToken: window.localStorage.getItem(REFRESH_TOKEN_KEY) || "",
  };
}

function saveTokens(tokens) {
  window.localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
  window.localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
}

function clearTokens() {
  window.localStorage.removeItem(ACCESS_TOKEN_KEY);
  window.localStorage.removeItem(REFRESH_TOKEN_KEY);
}

function extractErrorMessage(data, fallback) {
  if (typeof data === "string" && data.trim()) {
    return data;
  }
  if (data?.detail && typeof data.detail === "string") {
    return data.detail;
  }
  if (data?.detail?.message) {
    return data.detail.message;
  }
  if (data?.message) {
    return data.message;
  }
  return fallback;
}

async function parseResponse(response) {
  if (response.status === 204) {
    return null;
  }
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return response.json();
  }
  return response.text();
}

async function refreshPanelToken() {
  const { refreshToken } = readTokens();
  if (!refreshToken) {
    return false;
  }

  const response = await fetch("/panel-api/auth/refresh", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  const data = await parseResponse(response);
  if (!response.ok) {
    clearTokens();
    return false;
  }

  saveTokens(data);
  return true;
}

async function apiRequest(path, options = {}, settings = {}) {
  const { auth = true, retry = true } = settings;
  const headers = new Headers(options.headers || {});
  const body = options.body;

  if (!(body instanceof FormData) && body !== undefined && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  if (auth) {
    const { accessToken } = readTokens();
    if (accessToken) {
      headers.set("Authorization", `Bearer ${accessToken}`);
    }
  }

  const response = await fetch(path, {
    ...options,
    headers,
    body,
  });

  if (response.status === 401 && auth && retry) {
    const refreshed = await refreshPanelToken();
    if (refreshed) {
      return apiRequest(path, options, { ...settings, retry: false });
    }
  }

  const data = await parseResponse(response);
  if (!response.ok) {
    throw new Error(extractErrorMessage(data, `HTTP ${response.status}`));
  }
  return data;
}

function buildTemplateFromSchema(schema, components) {
  if (!schema) return null;
  if (schema.$ref) {
    const refName = schema.$ref.split("/").pop();
    return buildTemplateFromSchema(components?.[refName], components);
  }
  if (schema.example !== undefined) return schema.example;
  if (schema.default !== undefined) return schema.default;
  if (schema.enum?.length) return schema.enum[0];
  if (schema.allOf?.length) {
    return schema.allOf.reduce((acc, item) => {
      const next = buildTemplateFromSchema(item, components);
      if (next && typeof next === "object" && !Array.isArray(next)) {
        return { ...acc, ...next };
      }
      return acc;
    }, {});
  }
  if (schema.type === "object" || schema.properties) {
    const result = {};
    Object.entries(schema.properties || {}).forEach(([key, value]) => {
      result[key] = buildTemplateFromSchema(value, components);
    });
    return result;
  }
  if (schema.type === "array") {
    return [buildTemplateFromSchema(schema.items, components)];
  }
  if (schema.type === "integer" || schema.type === "number") return 0;
  if (schema.type === "boolean") return false;
  return "";
}

function operationId(method, path) {
  return `${method.toUpperCase()} ${path}`;
}

function humanizeValue(value) {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "boolean") return value ? "Да" : "Нет";
  return String(value);
}

function imageOrPlaceholder(url, alt) {
  return url ? <img src={url} alt={alt} /> : <div className="image-placeholder">Нет фото</div>;
}

function LoginPage({ onLogin, error, loading }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function submit(event) {
    event.preventDefault();
    await onLogin(email, password);
  }

  return (
    <div className="login-shell">
      <form className="login-card" onSubmit={submit}>
        <div>
          <p className="eyebrow">Новая админка</p>
          <h1>Вход для администратора</h1>
          <p className="muted">
            Войти может только суперпользователь. Публичный API и база остаются без изменений.
          </p>
        </div>

        <label className="field">
          <span>Email</span>
          <input value={email} onChange={(event) => setEmail(event.target.value)} type="email" required />
        </label>

        <label className="field">
          <span>Пароль</span>
          <input
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            type="password"
            required
          />
        </label>

        {error ? <p className="error-text">{error}</p> : null}

        <button className="primary-button" disabled={loading} type="submit">
          {loading ? "Входим..." : "Войти"}
        </button>
      </form>
    </div>
  );
}

function pagePathForSection(sectionId) {
  if (sectionId === "dashboard") return "/dashboard";
  if (sectionId === "actions") return "/actions";
  return null;
}

function Sidebar({ resources, sections, user, onLogout }) {
  const resourceSections = sections.filter((section) => section.kind === "group");
  const pageSections = sections.filter((section) => section.kind === "page");

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-mark">R</div>
        <div>
          <strong>Rahma</strong>
          <p>Admin Panel</p>
        </div>
      </div>

      <nav className="sidebar-nav">
        {pageSections.map((section) => {
          const path = pagePathForSection(section.id);
          if (!path) return null;
          return (
            <div className="sidebar-group" key={section.id}>
              <p className="sidebar-label">{section.label}</p>
              <NavLink className="sidebar-link" to={path}>
                {section.label}
              </NavLink>
            </div>
          );
        })}

        {resourceSections.map((section) => {
          const sectionResources = resources.filter((item) => item.section === section.id);
          if (!sectionResources.length) return null;
          return (
            <div className="sidebar-group" key={section.id}>
              <p className="sidebar-label">{section.label}</p>
              {sectionResources.map((resource) => (
                <NavLink key={resource.id} className="sidebar-link" to={`/resources/${resource.id}`}>
                  {resource.label}
                </NavLink>
              ))}
            </div>
          );
        })}
      </nav>

      <div className="sidebar-user">
        <div>
          <strong>{user.name}</strong>
          <p>{user.email}</p>
        </div>
        <button className="ghost-button" onClick={onLogout} type="button">
          Выйти
        </button>
      </div>
    </aside>
  );
}

function AppHeader({ title, description }) {
  return (
    <header className="page-header">
      <div>
        <p className="eyebrow">Rahma Admin</p>
        <h1>{title}</h1>
        {description ? <p className="muted">{description}</p> : null}
      </div>
    </header>
  );
}

function SummaryCard({ label, value, description }) {
  return (
    <article className="summary-card">
      <p className="eyebrow">{label}</p>
      <strong>{value}</strong>
      <span>{description}</span>
    </article>
  );
}

function DetailSection({ title, children, count, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <section className={`detail-accordion ${open ? "is-open" : ""}`}>
      <button
        className="detail-accordion-summary"
        onClick={() => setOpen((current) => !current)}
        type="button"
      >
        <span>{title}</span>
        <div className="detail-accordion-meta">
          {count !== undefined ? <span className="detail-accordion-count">{count}</span> : null}
          <span className="detail-accordion-toggle">{open ? "−" : "+"}</span>
        </div>
      </button>
      {open ? <div className="detail-accordion-body">{children}</div> : null}
    </section>
  );
}

function LinkedCard({ title, image, description, meta, onEdit, onDelete }) {
  return (
    <article className="linked-card">
      <div className="linked-card-head">
        <strong>{title}</strong>
        <div className="card-actions">
          <button className="icon-button" onClick={onEdit} type="button" title="Редактировать">
            ✎
          </button>
          <button className="icon-button danger" onClick={onDelete} type="button" title="Удалить">
            ×
          </button>
        </div>
      </div>
      <div className="linked-card-media">{imageOrPlaceholder(image, title)}</div>
      {description ? <p className="muted">{description}</p> : null}
      <div className="meta-list">
        {meta.map(([label, value]) => (
          <div key={label} className="meta-line">
            <span>{label}</span>
            <strong>{humanizeValue(value)}</strong>
          </div>
        ))}
      </div>
    </article>
  );
}

function AddTile({ label, onClick }) {
  return (
    <button className="add-tile" onClick={onClick} type="button">
      <span>+</span>
      <strong>{label}</strong>
    </button>
  );
}

function PreviewModal({ item, resource, onClose }) {
  if (!item || !resource) return null;

  const previewRows = resource.columns.map((column) => [column.label, item[column.key]]);

  return (
    <div className="modal-backdrop" onClick={onClose} role="presentation">
      <div className="modal-card preview-modal" onClick={(event) => event.stopPropagation()} role="dialog">
        <div className="modal-header">
          <div>
            <p className="eyebrow">{resource.singularLabel}</p>
            <h2>{item[resource.primaryField]}</h2>
          </div>
          <button className="ghost-button" onClick={onClose} type="button">
            Закрыть
          </button>
        </div>

        <div className="preview-layout">
          <div className="preview-media">
            {imageOrPlaceholder(resource.imageField ? item[resource.imageField] : "", item[resource.primaryField])}
          </div>
          <div className="detail-stack">
            {resource.descriptionField && item[resource.descriptionField] ? (
              <p className="muted">{item[resource.descriptionField]}</p>
            ) : null}
            <div className="detail-grid">
              {previewRows.map(([label, value]) => (
                <div key={label} className="detail-box">
                  <span>{label}</span>
                  <strong>{humanizeValue(value)}</strong>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function UploadField({ field, resource, value, onUploaded, onUploadError }) {
  const [uploading, setUploading] = useState(false);
  const [localError, setLocalError] = useState("");

  async function handleFile(file) {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    setUploading(true);
    setLocalError("");
    try {
      const result = await apiRequest(`/panel-api/uploads/${resource.entityType}`, {
        method: "POST",
        body: formData,
      });
      onUploaded(result.public_url);
    } catch (uploadError) {
      const message = uploadError.message || "Не удалось загрузить файл.";
      setLocalError(message);
      if (onUploadError) {
        onUploadError(message);
      }
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="field">
      <span>{field.label}</span>
      <label
        className={`dropzone ${uploading ? "is-uploading" : ""}`}
        onDragOver={(event) => {
          event.preventDefault();
        }}
        onDrop={(event) => {
          event.preventDefault();
          handleFile(event.dataTransfer.files?.[0]);
        }}
      >
        <input
          accept={field.accept?.join(",")}
          hidden
          onChange={(event) => handleFile(event.target.files?.[0])}
          type="file"
        />
        <strong>{uploading ? "Загрузка..." : "Перетащи файл или выбери изображение"}</strong>
        <p className="muted">JPG / PNG / WEBP / SVG</p>
      </label>
      {value ? (
        <div className="upload-preview">
          <div className="upload-preview-media">{imageOrPlaceholder(value, field.label)}</div>
          <p className="muted break-all">{value}</p>
        </div>
      ) : null}
      {field.helpText ? <p className="field-help">{field.helpText}</p> : null}
      {localError ? <p className="error-text">{localError}</p> : null}
    </div>
  );
}

function coerceFieldValue(field, value) {
  if (field.type === "boolean") {
    return Boolean(value);
  }
  if (field.type === "number") {
    return value === "" ? "" : Number(value);
  }
  return value;
}

function createInitialForm(resource, searchParams) {
  const values = {};
  resource.fields.forEach((field) => {
    if (field.type === "boolean") {
      values[field.name] = Boolean(field.default);
    } else if (field.default !== undefined && field.default !== null) {
      values[field.name] = field.default;
    } else {
      values[field.name] = "";
    }
    if (field.bind && values[field.bind] === undefined) {
      values[field.bind] = "";
    }
  });

  searchParams.forEach((value, key) => {
    if (key in values) {
      values[key] = value;
    }
  });

  return values;
}

function hydrateFormFromItem(resource, item, searchParams) {
  const values = createInitialForm(resource, searchParams);
  Object.keys(values).forEach((key) => {
    if (item[key] !== undefined && item[key] !== null) {
      values[key] = item[key];
    }
  });
  return values;
}

function buildPayload(resource, formValues) {
  const payload = {};
  resource.fields.forEach((field) => {
    if (field.type === "upload") {
      if (field.bind) {
        payload[field.bind] = formValues[field.bind] || "";
      }
      return;
    }
    if (field.type === "hidden") {
      return;
    }
    payload[field.name] = coerceFieldValue(field, formValues[field.name]);
  });
  return payload;
}

function ResourcePage({ resources }) {
  const navigate = useNavigate();
  const { resourceId } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const resource = resources.find((item) => item.id === resourceId);
  const [items, setItems] = useState([]);
  const [optionsMap, setOptionsMap] = useState({});
  const [formValues, setFormValues] = useState({});
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const editItemId = searchParams.get("item");
  const previewItemId = searchParams.get("preview");
  const mode = searchParams.get("mode") || "create";

  useEffect(() => {
    if (!resource) return;

    let cancelled = false;

    async function load() {
      setLoading(true);
      try {
        const [loadedItems, optionEntries] = await Promise.all([
          apiRequest(`/panel-api/resources/${resource.id}/items`),
          Promise.all(
            resource.fields
              .filter((field) => field.optionsResource)
              .map(async (field) => [
                field.optionsResource,
                await apiRequest(`/panel-api/resources/${field.optionsResource}/options`),
              ]),
          ),
        ]);

        if (cancelled) return;
        setItems(loadedItems);
        setOptionsMap(Object.fromEntries(optionEntries));
      } catch (loadError) {
        if (!cancelled) {
          setError(loadError.message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [resource]);

  useEffect(() => {
    if (!resource) return;
    if (mode === "edit" && editItemId) {
      const currentItem = items.find((item) => String(item.id) === editItemId);
      if (currentItem) {
        setFormValues(hydrateFormFromItem(resource, currentItem, searchParams));
        return;
      }
    }
    setFormValues(createInitialForm(resource, searchParams));
  }, [resource, items, editItemId, mode, searchParams]);

  if (!resource) {
    return (
      <section className="page-section">
        <AppHeader title="Ресурс не найден" description="Проверь идентификатор раздела." />
      </section>
    );
  }

  const previewItem = items.find((item) => String(item.id) === previewItemId);

  async function refreshItems() {
    const loadedItems = await apiRequest(`/panel-api/resources/${resource.id}/items`);
    setItems(loadedItems);
  }

  async function submitForm(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      const payload = buildPayload(resource, formValues);
      if (mode === "edit" && editItemId) {
        await apiRequest(`/panel-api/resources/${resource.id}/items/${editItemId}`, {
          method: "PATCH",
          body: JSON.stringify(payload),
        });
      } else {
        await apiRequest(`/panel-api/resources/${resource.id}/items`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }
      await refreshItems();
      setSearchParams((current) => {
        const next = new URLSearchParams(current);
        next.set("mode", "create");
        next.delete("item");
        return next;
      });
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setSaving(false);
    }
  }

  async function deleteItem(itemId) {
    if (!window.confirm(`Удалить ${resource.singularLabel.toLowerCase()}?`)) return;
    await apiRequest(`/panel-api/resources/${resource.id}/items/${itemId}`, { method: "DELETE" });
    await refreshItems();
    setSearchParams((current) => {
      const next = new URLSearchParams(current);
      if (next.get("item") === String(itemId)) {
        next.delete("item");
        next.set("mode", "create");
      }
      if (next.get("preview") === String(itemId)) {
        next.delete("preview");
      }
      return next;
    });
  }

  function openEdit(itemId) {
    setSearchParams((current) => {
      const next = new URLSearchParams(current);
      next.set("mode", "edit");
      next.set("item", itemId);
      return next;
    });
  }

  function openPreview(itemId) {
    setSearchParams((current) => {
      const next = new URLSearchParams(current);
      next.set("preview", itemId);
      return next;
    });
  }

  function closePreview() {
    setSearchParams((current) => {
      const next = new URLSearchParams(current);
      next.delete("preview");
      return next;
    });
  }

  function resetForm() {
    setSearchParams((current) => {
      const next = new URLSearchParams(current);
      next.set("mode", "create");
      next.delete("item");
      return next;
    });
  }

  function renderField(field) {
    if (field.type === "hidden") return null;
    if (field.type === "upload") {
      return (
        <UploadField
          field={field}
          key={field.name}
          onUploadError={(message) => setError(message)}
          onUploaded={(url) =>
            {
              setError("");
              setFormValues((current) => ({
                ...current,
                [field.bind]: url,
              }));
            }
          }
          resource={resource}
          value={formValues[field.bind] || ""}
        />
      );
    }

    const fieldValue = formValues[field.name] ?? (field.type === "boolean" ? false : "");
    const options = field.optionsResource ? optionsMap[field.optionsResource] || [] : field.options || [];

    return (
      <label
        className={`field ${field.type === "textarea" || field.type === "boolean" ? "form-span" : ""}`}
        key={field.name}
      >
        <span>{field.label}</span>
        {field.type === "textarea" ? (
          <textarea
            onChange={(event) =>
              setFormValues((current) => ({ ...current, [field.name]: event.target.value }))
            }
            placeholder={field.placeholder}
            required={field.required}
            rows={5}
            value={fieldValue}
          />
        ) : null}

        {field.type === "text" ? (
          <input
            onChange={(event) =>
              setFormValues((current) => ({ ...current, [field.name]: event.target.value }))
            }
            placeholder={field.placeholder}
            required={field.required}
            type="text"
            value={fieldValue}
          />
        ) : null}

        {field.type === "number" ? (
          <input
            max={field.max}
            min={field.min}
            onChange={(event) =>
              setFormValues((current) => ({ ...current, [field.name]: event.target.value }))
            }
            placeholder={field.placeholder}
            required={field.required}
            step={field.step || "any"}
            type="number"
            value={fieldValue}
          />
        ) : null}

        {field.type === "select" ? (
          <select
            onChange={(event) =>
              setFormValues((current) => ({ ...current, [field.name]: event.target.value }))
            }
            required={field.required}
            value={fieldValue}
          >
            <option value="">Выбери значение</option>
            {options.map((option) => (
              <option key={`${field.name}-${option.value}`} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        ) : null}

        {field.type === "boolean" ? (
          <div className="checkbox-row">
            <input
              checked={Boolean(fieldValue)}
              onChange={(event) =>
                setFormValues((current) => ({ ...current, [field.name]: event.target.checked }))
              }
              type="checkbox"
            />
            <span>{field.label}</span>
          </div>
        ) : null}

        {field.helpText ? <p className="field-help">{field.helpText}</p> : null}
      </label>
    );
  }

  return (
    <section className="page-section">
      <AppHeader
        title={resource.label}
        description="Список, просмотр, создание, редактирование и удаление в одном разделе."
      />

      <div className="page-grid">
        <div className="page-panel">
          <div className="panel-head">
            <div>
              <p className="eyebrow">Форма</p>
              <h2>{mode === "edit" ? `Редактирование: ${resource.singularLabel}` : resource.createLabel}</h2>
            </div>
            {mode === "edit" ? (
              <button className="ghost-button" onClick={resetForm} type="button">
                Отменить
              </button>
            ) : null}
          </div>

          <form className="form-grid" onSubmit={submitForm}>
            {resource.fields.map(renderField)}
            {error ? <p className="error-text form-span">{error}</p> : null}
            <div className="form-actions form-span">
              <button className="primary-button" disabled={saving} type="submit">
                {saving ? "Сохраняем..." : mode === "edit" ? "Сохранить изменения" : resource.createLabel}
              </button>
            </div>
          </form>
        </div>

        <div className="page-panel">
          <div className="panel-head">
            <div>
              <p className="eyebrow">Список</p>
              <h2>{resource.label}</h2>
            </div>
            <button className="ghost-button" onClick={refreshItems} type="button">
              Обновить
            </button>
          </div>

          {loading ? <p className="muted">Загружаем...</p> : null}

          <div className="resource-grid">
            <AddTile
              label={resource.createLabel}
              onClick={() => {
                resetForm();
                navigate(`/resources/${resource.id}?mode=create`);
              }}
            />

            {items.map((item) => (
              <article className="resource-card" key={item.id}>
                <div className="resource-card-head">
                  <strong>{item[resource.primaryField]}</strong>
                  <div className="card-actions">
                    <button
                      className="icon-button"
                      onClick={() => openPreview(String(item.id))}
                      title="Просмотр"
                      type="button"
                    >
                      👁
                    </button>
                    <button
                      className="icon-button"
                      onClick={() => openEdit(String(item.id))}
                      title="Редактировать"
                      type="button"
                    >
                      ✎
                    </button>
                    <button
                      className="icon-button danger"
                      onClick={() => deleteItem(item.id)}
                      title="Удалить"
                      type="button"
                    >
                      ×
                    </button>
                  </div>
                </div>
                {resource.imageField ? (
                  <div className="resource-card-media">
                    {imageOrPlaceholder(item[resource.imageField], item[resource.primaryField])}
                  </div>
                ) : null}
                {resource.descriptionField && item[resource.descriptionField] ? (
                  <p className="muted">{String(item[resource.descriptionField]).slice(0, 140)}</p>
                ) : null}
                <div className="meta-list">
                  {resource.columns.map((column) => (
                    <div className="meta-line" key={`${item.id}-${column.key}`}>
                      <span>{column.label}</span>
                      <strong>{humanizeValue(item[column.key])}</strong>
                    </div>
                  ))}
                </div>
              </article>
            ))}
          </div>

          {!loading && items.length === 0 ? <p className="muted">{resource.emptyState}</p> : null}
        </div>
      </div>

      <PreviewModal item={previewItem} onClose={closePreview} resource={resource} />
    </section>
  );
}

function ActionExplorer({ actionCatalog }) {
  const [searchParams, setSearchParams] = useSearchParams();
  const [filter, setFilter] = useState("");
  const [pathParams, setPathParams] = useState({});
  const [queryParams, setQueryParams] = useState({});
  const [bodyText, setBodyText] = useState("");
  const [useCurrentAuth, setUseCurrentAuth] = useState(true);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const operations = [];
  Object.entries(actionCatalog?.paths || {}).forEach(([path, methods]) => {
    Object.entries(methods).forEach(([method, details]) => {
      operations.push({
        id: operationId(method, path),
        path,
        method,
        ...details,
      });
    });
  });

  const filteredOperations = operations.filter((operation) => {
    const haystack = `${operation.method} ${operation.path} ${operation.summary || ""} ${(operation.tags || []).join(" ")}`.toLowerCase();
    return haystack.includes(filter.toLowerCase());
  });

  const selectedOperationId = searchParams.get("operation") || filteredOperations[0]?.id || "";
  const selectedOperation = operations.find((item) => item.id === selectedOperationId) || null;
  const bodySchema = selectedOperation?.requestBody?.content?.["application/json"]?.schema;

  useEffect(() => {
    if (!selectedOperation) return;
    const nextPath = {};
    const nextQuery = {};
    (selectedOperation.parameters || []).forEach((parameter) => {
      if (parameter.in === "path") nextPath[parameter.name] = "";
      if (parameter.in === "query") nextQuery[parameter.name] = "";
    });
    setPathParams(nextPath);
    setQueryParams(nextQuery);
    const template = buildTemplateFromSchema(bodySchema, actionCatalog?.components?.schemas);
    setBodyText(template === null ? "" : JSON.stringify(template, null, 2));
    setResult(null);
    setError("");
  }, [selectedOperationId]);

  async function executeOperation(event) {
    event.preventDefault();
    if (!selectedOperation) return;
    setRunning(true);
    setError("");
    try {
      const jsonBody = bodyText.trim() ? JSON.parse(bodyText) : null;
      const response = await apiRequest("/panel-api/actions/execute", {
        method: "POST",
        body: JSON.stringify({
          method: selectedOperation.method.toUpperCase(),
          path: selectedOperation.path,
          pathParams: pathParams,
          queryParams: queryParams,
          jsonBody,
          useCurrentAuth,
        }),
      });
      setResult(response);
    } catch (runError) {
      setError(runError.message);
      setResult(null);
    } finally {
      setRunning(false);
    }
  }

  return (
    <section className="page-section">
      <AppHeader
        title="API методы"
        description="Универсальный интерфейс для всех текущих /api/v1 методов без изменения публичного API."
      />

      <div className="page-grid">
        <div className="page-panel explorer-list">
          <div className="panel-head">
            <div>
              <p className="eyebrow">Каталог</p>
              <h2>Методы API</h2>
            </div>
          </div>

          <label className="field">
            <span>Поиск</span>
            <input
              onChange={(event) => setFilter(event.target.value)}
              placeholder="Например: routes, auth, messages"
              type="text"
              value={filter}
            />
          </label>

          <div className="operation-list">
            {filteredOperations.map((operation) => (
              <button
                className={`operation-item ${operation.id === selectedOperationId ? "is-active" : ""}`}
                key={operation.id}
                onClick={() => setSearchParams({ operation: operation.id })}
                type="button"
              >
                <strong>
                  {operation.method.toUpperCase()} {operation.path}
                </strong>
                <span>{operation.summary || "Без описания"}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="page-panel">
          {!selectedOperation ? (
            <p className="muted">Нет доступных методов API.</p>
          ) : (
            <>
              <div className="panel-head">
                <div>
                  <p className="eyebrow">{(selectedOperation.tags || []).join(", ") || "API"}</p>
                  <h2>
                    {selectedOperation.method.toUpperCase()} {selectedOperation.path}
                  </h2>
                  <p className="muted">{selectedOperation.summary || selectedOperation.description}</p>
                </div>
              </div>

              <form className="form-grid" onSubmit={executeOperation}>
                {(selectedOperation.parameters || [])
                  .filter((parameter) => parameter.in === "path")
                  .map((parameter) => (
                    <label className="field" key={`path-${parameter.name}`}>
                      <span>Path: {parameter.name}</span>
                      <input
                        onChange={(event) =>
                          setPathParams((current) => ({ ...current, [parameter.name]: event.target.value }))
                        }
                        required={parameter.required}
                        type="text"
                        value={pathParams[parameter.name] || ""}
                      />
                    </label>
                  ))}

                {(selectedOperation.parameters || [])
                  .filter((parameter) => parameter.in === "query")
                  .map((parameter) => (
                    <label className="field" key={`query-${parameter.name}`}>
                      <span>Query: {parameter.name}</span>
                      <input
                        onChange={(event) =>
                          setQueryParams((current) => ({ ...current, [parameter.name]: event.target.value }))
                        }
                        required={parameter.required}
                        type="text"
                        value={queryParams[parameter.name] || ""}
                      />
                    </label>
                  ))}

                {bodySchema ? (
                  <label className="field form-span">
                    <span>JSON body</span>
                    <textarea
                      onChange={(event) => setBodyText(event.target.value)}
                      rows={12}
                      value={bodyText}
                    />
                  </label>
                ) : null}

                <label className="field form-span">
                  <div className="checkbox-row">
                    <input
                      checked={useCurrentAuth}
                      onChange={(event) => setUseCurrentAuth(event.target.checked)}
                      type="checkbox"
                    />
                    <span>Пробросить текущий admin token в вызов метода</span>
                  </div>
                </label>

                {error ? <p className="error-text form-span">{error}</p> : null}

                <div className="form-actions form-span">
                  <button className="primary-button" disabled={running} type="submit">
                    {running ? "Выполняем..." : "Выполнить метод"}
                  </button>
                </div>
              </form>

              <div className="response-panel">
                <div className="panel-head">
                  <div>
                    <p className="eyebrow">Ответ</p>
                    <h2>{result ? `HTTP ${result.statusCode}` : "Результат появится после запуска"}</h2>
                  </div>
                </div>
                <pre>{result ? JSON.stringify(result.body, null, 2) : "—"}</pre>
              </div>
            </>
          )}
        </div>
      </div>
    </section>
  );
}

function DashboardPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [summary, setSummary] = useState(null);
  const [countries, setCountries] = useState([]);
  const [routeResources, setRouteResources] = useState([]);
  const [routes, setRoutes] = useState([]);
  const [routeDetail, setRouteDetail] = useState(null);
  const [routeHotels, setRouteHotels] = useState([]);
  const [routeRestaurants, setRouteRestaurants] = useState([]);
  const selectedCountryId = searchParams.get("country");
  const selectedRouteId = searchParams.get("route");
  const selectedCountry = countries.find((item) => String(item.id) === selectedCountryId) || null;
  const selectedRouteResource =
    routeResources.find((item) => String(item.id) === String(selectedRouteId)) || null;

  async function loadSummary() {
    const [summaryData, countriesData, routeResourceData] = await Promise.all([
      apiRequest("/panel-api/dashboard"),
      apiRequest("/panel-api/resources/countries/items"),
      apiRequest("/panel-api/resources/routes/items"),
    ]);
    setSummary(summaryData);
    setCountries(countriesData);
    setRouteResources(routeResourceData);
  }

  useEffect(() => {
    loadSummary().catch((error) => window.alert(error.message));
  }, []);

  useEffect(() => {
    if (!selectedCountryId) {
      setRoutes([]);
      setRouteDetail(null);
      setRouteHotels([]);
      setRouteRestaurants([]);
      return;
    }

    let cancelled = false;

    async function loadCountryRoutes() {
      const response = await apiRequest(`/api/v1/routes?limit=100&offset=0&country=${selectedCountryId}`, {}, { auth: false });
      if (cancelled) return;
      const loadedRoutes = response.items || [];
      setRoutes(loadedRoutes);

      if (!loadedRoutes.some((item) => String(item.id) === selectedRouteId) && loadedRoutes[0]) {
        setSearchParams((current) => {
          const next = new URLSearchParams(current);
          next.set("country", selectedCountryId);
          next.set("route", loadedRoutes[0].id);
          return next;
        });
      }
    }

    loadCountryRoutes().catch((error) => window.alert(error.message));
    return () => {
      cancelled = true;
    };
  }, [selectedCountryId]);

  useEffect(() => {
    if (!selectedRouteId) {
      setRouteDetail(null);
      setRouteHotels([]);
      setRouteRestaurants([]);
      return;
    }

    let cancelled = false;

    async function loadBundle() {
      const [detail, hotels, restaurants] = await Promise.all([
        apiRequest(`/api/v1/routes/${selectedRouteId}`, {}, { auth: false }),
        apiRequest(`/api/v1/routes/${selectedRouteId}/hotels`, {}, { auth: false }),
        apiRequest(`/api/v1/routes/${selectedRouteId}/restaurants`, {}, { auth: false }),
      ]);
      if (cancelled) return;
      setRouteDetail(detail);
      setRouteHotels(hotels.items || []);
      setRouteRestaurants(restaurants.items || []);
    }

    loadBundle().catch((error) => window.alert(error.message));
    return () => {
      cancelled = true;
    };
  }, [selectedRouteId]);

  async function deleteResource(resourceId, itemId, message) {
    if (!window.confirm(message)) return;
    await apiRequest(`/panel-api/resources/${resourceId}/items/${itemId}`, { method: "DELETE" });
    await loadSummary();
    if (resourceId === "routes" && selectedCountryId) {
      const response = await apiRequest(`/api/v1/routes?limit=100&offset=0&country=${selectedCountryId}`, {}, { auth: false });
      const nextRoutes = response.items || [];
      setRoutes(nextRoutes);
      if (String(selectedRouteId) === String(itemId)) {
        setSearchParams((current) => {
          const next = new URLSearchParams(current);
          if (nextRoutes[0]?.id) {
            next.set("route", nextRoutes[0].id);
          } else {
            next.delete("route");
          }
          return next;
        });
      }
    }
    if (selectedRouteId) {
      const [hotels, restaurants] = await Promise.all([
        apiRequest(`/api/v1/routes/${selectedRouteId}/hotels`, {}, { auth: false }),
        apiRequest(`/api/v1/routes/${selectedRouteId}/restaurants`, {}, { auth: false }),
      ]);
      setRouteHotels(hotels.items || []);
      setRouteRestaurants(restaurants.items || []);
    }
  }

  return (
    <section className="page-section">
      <AppHeader
        title="Дашборд"
        description="Быстрый обзор стран, маршрутов и связанных сущностей. Все данные читаются из той же базы и того же API."
      />

      <div className="summary-grid">
        <SummaryCard description="Карточки стран" label="Страны" value={summary?.countries || 0} />
        <SummaryCard description="Основа контента" label="Маршруты" value={summary?.routes || 0} />
        <SummaryCard description="С привязкой к маршрутам" label="Отели" value={summary?.hotels || 0} />
        <SummaryCard description="С прямой загрузкой фото" label="Рестораны" value={summary?.restaurants || 0} />
      </div>

      <div className="page-panel">
        <div className="panel-head">
          <div>
            <p className="eyebrow">Страны</p>
            <h2>Навигация по контенту</h2>
          </div>
        </div>
        <div className="country-grid">
          {countries.map((country) => (
            <button
              className="country-card"
              key={country.id}
              onClick={() =>
                setSearchParams((current) => {
                  const next = new URLSearchParams(current);
                  next.set("country", country.id);
                  next.delete("route");
                  return next;
                })
              }
              type="button"
            >
              <div className="country-card-media">{imageOrPlaceholder(country.photoUrl, country.name)}</div>
              <div className="country-card-body">
                <strong>{country.name}</strong>
                <span>Маршрутов: {country.routes_count}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {selectedCountry ? (
        <div
          className="modal-backdrop"
          onClick={() => {
            setSearchParams({});
          }}
          role="presentation"
        >
          <div className="modal-card explorer-modal" onClick={(event) => event.stopPropagation()} role="dialog">
            <div className="modal-header">
              <div>
                <p className="eyebrow">{selectedCountry.name}</p>
                <h2>{selectedCountry.name}</h2>
              </div>
              <button className="ghost-button" onClick={() => setSearchParams({})} type="button">
                Закрыть
              </button>
            </div>

            <div className="explorer-layout">
              <aside className="explorer-sidebar">
                <div className="sidebar-head">
                  <h3>Маршруты</h3>
                  <span>{routes.length}</span>
                </div>
                <AddTile
                  label="Добавить маршрут"
                  onClick={() => navigate(`/resources/routes?mode=create&countryId=${selectedCountry.id}`)}
                />
                <div className="route-list">
                  {routes.map((route) => (
                    <button
                      className={`route-list-item ${route.id === selectedRouteId ? "is-active" : ""}`}
                      key={route.id}
                      onClick={() =>
                        setSearchParams((current) => {
                          const next = new URLSearchParams(current);
                          next.set("country", selectedCountry.id);
                          next.set("route", route.id);
                          return next;
                        })
                      }
                      type="button"
                    >
                      <strong>{route.name}</strong>
                      <p>{route.category}</p>
                      <span>{String(route.content || "").slice(0, 100)}</span>
                    </button>
                  ))}
                </div>
              </aside>

              <div className="explorer-content">
                {!routeDetail ? (
                  <div className="page-panel">
                    <p className="muted">У этой страны пока нет маршрутов.</p>
                  </div>
                ) : (
                  <>
                    <article className="detail-hero">
                      <div className="detail-hero-image">
                        {imageOrPlaceholder(selectedRouteResource?.photoUrl || "", routeDetail.name)}
                      </div>
                      <div className="detail-hero-copy">
                        <div className="detail-head">
                          <div>
                            <p className="eyebrow">{routeDetail.country?.name || selectedCountry.name}</p>
                            <h3>{routeDetail.name}</h3>
                          </div>
                          <div className="card-actions">
                            <button
                              className="icon-button"
                              onClick={() => navigate(`/resources/routes?mode=edit&item=${routeDetail.id}`)}
                              type="button"
                            >
                              ✎
                            </button>
                            <button
                              className="icon-button danger"
                              onClick={() => deleteResource("routes", routeDetail.id, "Удалить маршрут?")}
                              type="button"
                            >
                              ×
                            </button>
                          </div>
                        </div>
                        <div className="chip-row">
                          <span className="chip">{routeDetail.category}</span>
                          <span className="chip">Отелей: {routeDetail.hotelsCount}</span>
                          <span className="chip">Ресторанов: {routeDetail.restaurantsCount}</span>
                        </div>
                        <p className="muted">{routeDetail.content}</p>
                      </div>
                    </article>

                    <section className="page-panel">
                      <div className="panel-head">
                        <div>
                          <p className="eyebrow">Отели</p>
                          <h3>Связанные отели</h3>
                        </div>
                        <span className="detail-accordion-count">{routeHotels.length}</span>
                      </div>
                      <div className="detail-section-grid">
                        <AddTile
                          label="Добавить отель"
                          onClick={() => navigate(`/resources/hotels?mode=create&routeId=${routeDetail.id}`)}
                        />
                        {routeHotels.length ? (
                          routeHotels.map((hotel) => (
                            <LinkedCard
                              description={hotel.description}
                              image={hotel.photoUrl}
                              key={hotel.id}
                              meta={[
                                ["Рейтинг", hotel.avgScore],
                                ["Оценок", hotel.scoreCount],
                                ["Цена", hotel.avgPrice],
                                ["Координаты", `${hotel.location?.lat}, ${hotel.location?.lng}`],
                              ]}
                              onDelete={() => deleteResource("hotels", hotel.id, "Удалить отель?")}
                              onEdit={() => navigate(`/resources/hotels?mode=edit&item=${hotel.id}`)}
                              title={hotel.name}
                            />
                          ))
                        ) : (
                          <p className="muted">У маршрута пока нет отелей.</p>
                        )}
                      </div>
                    </section>

                    <section className="page-panel">
                      <div className="panel-head">
                        <div>
                          <p className="eyebrow">Рестораны</p>
                          <h3>Связанные рестораны</h3>
                        </div>
                        <span className="detail-accordion-count">{routeRestaurants.length}</span>
                      </div>
                      <div className="detail-section-grid">
                        <AddTile
                          label="Добавить ресторан"
                          onClick={() => navigate(`/resources/restaurants?mode=create&routeId=${routeDetail.id}`)}
                        />
                        {routeRestaurants.length ? (
                          routeRestaurants.map((restaurant) => (
                            <LinkedCard
                              description={restaurant.description}
                              image={restaurant.photoUrl}
                              key={restaurant.id}
                              meta={[
                                ["Рейтинг", restaurant.avgScore],
                                ["Оценок", restaurant.scoreCount],
                                ["Цена", restaurant.costLevel],
                                ["Харам", restaurant.isHaram ? "Да" : "Нет"],
                              ]}
                              onDelete={() => deleteResource("restaurants", restaurant.id, "Удалить ресторан?")}
                              onEdit={() => navigate(`/resources/restaurants?mode=edit&item=${restaurant.id}`)}
                              title={restaurant.name}
                            />
                          ))
                        ) : (
                          <p className="muted">У маршрута пока нет ресторанов.</p>
                        )}
                      </div>
                    </section>

                    <section className="page-panel">
                      <div className="panel-head">
                        <div>
                          <p className="eyebrow">Галерея маршрута</p>
                          <h3>Изображения</h3>
                        </div>
                      </div>
                      <div className="detail-section-grid">
                        {(routeDetail.images || []).length ? (
                          routeDetail.images.map((image) => (
                            <article className="gallery-card" key={image.id || image.url}>
                              {imageOrPlaceholder(image.url, routeDetail.name)}
                              <p className="muted break-all">{image.url}</p>
                            </article>
                          ))
                        ) : (
                          <p className="muted">Дополнительные изображения пока не добавлены.</p>
                        )}
                      </div>
                    </section>

                    <section className="page-panel">
                      <div className="panel-head">
                        <div>
                          <p className="eyebrow">Шаблоны амалей</p>
                          <h3>Связанный контент</h3>
                        </div>
                      </div>
                      {(routeDetail.amalTemplates || []).length ? (
                        <ul className="template-list">
                          {routeDetail.amalTemplates.map((item) => (
                            <li key={item.id || item.title}>
                              <strong>{item.title}</strong>
                              {item.reccuringRule ? <span>{item.reccuringRule}</span> : null}
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <p className="muted">Шаблонов амалей пока нет.</p>
                      )}
                    </section>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}

function Shell({ resources, user, onLogout }) {
  const { actions, sections } = useBootstrap();

  return (
    <div className="app-shell">
      <Sidebar onLogout={onLogout} resources={resources} sections={sections} user={user} />
      <main className="content-shell">
        <Routes>
          <Route element={<Navigate replace to="/dashboard" />} path="/" />
          <Route element={<DashboardPage />} path="/dashboard" />
          <Route element={<ResourcePage resources={resources} />} path="/resources/:resourceId" />
          <Route element={<ActionExplorer actionCatalog={actions} />} path="/actions" />
          <Route element={<Navigate replace to="/dashboard" />} path="*" />
        </Routes>
      </main>
    </div>
  );
}

function useBootstrap() {
  return useContext(BootstrapContext);
}

export default function App() {
  const [authState, setAuthState] = useState({ loading: true, user: null });
  const [meta, setMeta] = useState({ resources: [], actions: {}, sections: [] });
  const [loginError, setLoginError] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);

  async function loadBootstrap() {
    const bootstrap = await apiRequest("/panel-api/meta/bootstrap");
    setMeta({ resources: bootstrap.resources, actions: bootstrap.actions, sections: bootstrap.sections });
    setAuthState({ loading: false, user: bootstrap.user });
  }

  useEffect(() => {
    let cancelled = false;

    async function bootstrap() {
      const { accessToken } = readTokens();
      if (!accessToken) {
        if (!cancelled) {
          setAuthState({ loading: false, user: null });
        }
        return;
      }

      try {
        await loadBootstrap();
      } catch (error) {
        clearTokens();
        if (!cancelled) {
          setAuthState({ loading: false, user: null });
        }
      }
    }

    bootstrap();
    return () => {
      cancelled = true;
    };
  }, []);

  async function handleLogin(email, password) {
    setLoginLoading(true);
    setLoginError("");
    try {
      const result = await apiRequest(
        "/panel-api/auth/login",
        {
          method: "POST",
          body: JSON.stringify({ email, password }),
        },
        { auth: false, retry: false },
      );
      saveTokens(result);
      await loadBootstrap();
    } catch (error) {
      setLoginError(error.message);
    } finally {
      setLoginLoading(false);
    }
  }

  async function handleLogout() {
    const { refreshToken } = readTokens();
    try {
      if (refreshToken) {
        await apiRequest(
          "/panel-api/auth/logout",
          {
            method: "POST",
            body: JSON.stringify({ refresh_token: refreshToken }),
          },
          { auth: false, retry: false },
        );
      }
    } finally {
      clearTokens();
      setAuthState({ loading: false, user: null });
      setMeta({ resources: [], actions: {}, sections: [] });
    }
  }

  if (authState.loading) {
    return (
      <div className="loading-shell">
        <div className="loading-card">Загружаем новую админку...</div>
      </div>
    );
  }

  if (!authState.user) {
    return <LoginPage error={loginError} loading={loginLoading} onLogin={handleLogin} />;
  }

  return (
    <BootstrapContext.Provider value={meta}>
      <Shell onLogout={handleLogout} resources={meta.resources} user={authState.user} />
    </BootstrapContext.Provider>
  );
}
