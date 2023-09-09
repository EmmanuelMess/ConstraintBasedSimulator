#ifndef CONSTRAINTBASEDSIMULATOR_SIGNAL_HPP
#define CONSTRAINTBASEDSIMULATOR_SIGNAL_HPP

#include <vector>
#include <functional>

template<typename Signature>
class Signal {
public:
    inline void connect(const std::function<Signature>& function) {
        callbacks.push_back(function);
    }

    inline void disconnect(const std::function<Signature>& function) {
        std::erase_if(callbacks, [&function](const std::function<Signature>& callback) {
            return getAddress(callback) == getAddress(function);
        });
    }

    template<typename... Args>
    inline void operator()(Args... args) const {
        for (const auto& callback : callbacks) {
            callback(args...);
        }
    }
private:
    std::vector<std::function<Signature>> callbacks;

    template<typename T, typename... U>
    static inline std::optional<std::size_t> getAddress(std::function<T(U...)> function) {
        using fnType = T(*)(U...);
        fnType ** fnPointer = function.template target<fnType*>();
        if(fnPointer) {
            return { reinterpret_cast<std::size_t>(*fnPointer) };
        }
        return { };
    }
};

#endif// CONSTRAINTBASEDSIMULATOR_SIGNAL_HPP
